import os
import stripe
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

from src.routes.auth import token_required
from src.models.subscription import db, Plan, Subscription

# Initialize Stripe with the API key
stripe.api_key = os.getenv('STRIPE_API_KEY', 'sk_test_51NxSampleStripeKeyForDevelopment')

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/create-checkout-session', methods=['POST'])
@token_required
def create_checkout_session(current_user):
    """Create a Stripe checkout session for subscription payment"""
    data = request.get_json()
    
    if not data or 'plan_id' not in data:
        return jsonify({'message': 'Plan ID is required!'}), 400
    
    # Get the plan details
    plan = Plan.query.get(data['plan_id'])
    if not plan:
        return jsonify({'message': 'Plan not found!'}), 404
    
    if not plan.is_active:
        return jsonify({'message': 'This plan is no longer available!'}), 400
    
    # Check if user already has an active subscription
    existing_subscription = Subscription.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).first()
    
    if existing_subscription:
        return jsonify({'message': 'User already has an active subscription!'}), 409
    
    try:
        # Create a Stripe product if it doesn't exist
        stripe_product = stripe.Product.create(
            name=f"Marketing Platform - {plan.name} Plan",
            description=plan.description
        )
        
        # Create a Stripe price for the product
        stripe_price = stripe.Price.create(
            product=stripe_product.id,
            unit_amount=int(plan.price * 100),  # Convert to cents
            currency='usd',
            recurring={
                'interval': 'month' if plan.billing_cycle == 'monthly' else 'year'
            }
        )
        
        # Create a checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': stripe_price.id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f"{request.host_url}payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{request.host_url}payment/cancel",
            client_reference_id=current_user.id,
            metadata={
                'plan_id': plan.id
            }
        )
        
        return jsonify({
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error creating checkout session: {str(e)}'}), 500

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_sample_webhook_secret_for_development')
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'message': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'message': 'Invalid signature'}), 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Get user and plan from session metadata
        user_id = session.get('client_reference_id')
        plan_id = session.get('metadata', {}).get('plan_id')
        
        if user_id and plan_id:
            # Create a new subscription
            subscription = Subscription(
                user_id=user_id,
                plan_id=plan_id,
                status='active',
                payment_method_id=session.get('payment_intent'),
                stripe_subscription_id=session.get('subscription')
            )
            
            # Set end date based on plan billing cycle
            plan = Plan.query.get(plan_id)
            if plan:
                if plan.billing_cycle == 'monthly':
                    subscription.end_date = datetime.utcnow() + timedelta(days=30)
                elif plan.billing_cycle == 'yearly':
                    subscription.end_date = datetime.utcnow() + timedelta(days=365)
            
            db.session.add(subscription)
            db.session.commit()
    
    elif event['type'] == 'customer.subscription.updated':
        subscription_data = event['data']['object']
        
        # Update subscription status
        subscription = Subscription.query.filter_by(
            stripe_subscription_id=subscription_data.get('id')
        ).first()
        
        if subscription:
            subscription.status = subscription_data.get('status', 'active')
            db.session.commit()
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription_data = event['data']['object']
        
        # Cancel subscription
        subscription = Subscription.query.filter_by(
            stripe_subscription_id=subscription_data.get('id')
        ).first()
        
        if subscription:
            subscription.status = 'canceled'
            db.session.commit()
    
    return jsonify({'status': 'success'}), 200

@payment_bp.route('/success', methods=['GET'])
def payment_success():
    """Handle successful payment"""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return jsonify({'message': 'Session ID is required!'}), 400
    
    try:
        # Retrieve the session
        session = stripe.checkout.Session.retrieve(session_id)
        
        return jsonify({
            'message': 'Payment successful!',
            'subscription_id': session.get('subscription')
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error retrieving session: {str(e)}'}), 500

@payment_bp.route('/cancel', methods=['GET'])
def payment_cancel():
    """Handle canceled payment"""
    return jsonify({'message': 'Payment canceled!'}), 200

@payment_bp.route('/customer-portal', methods=['POST'])
@token_required
def customer_portal(current_user):
    """Create a Stripe customer portal session for subscription management"""
    # Get the user's active subscription
    subscription = Subscription.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).first()
    
    if not subscription or not subscription.stripe_subscription_id:
        return jsonify({'message': 'No active subscription found!'}), 404
    
    try:
        # Retrieve the Stripe subscription to get the customer ID
        stripe_subscription = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
        
        # Create a customer portal session
        portal_session = stripe.billing_portal.Session.create(
            customer=stripe_subscription.customer,
            return_url=f"{request.host_url}account/billing"
        )
        
        return jsonify({
            'portal_url': portal_session.url
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error creating customer portal: {str(e)}'}), 500
