from flask import Blueprint, request, jsonify
from datetime import datetime

from src.routes.auth import token_required
from src.models.subscription import db, Plan, Subscription

subscriptions_bp = Blueprint('subscriptions', __name__)

@subscriptions_bp.route('/plans', methods=['GET'])
def get_plans():
    """Get all available subscription plans"""
    plans = Plan.query.filter_by(is_active=True).all()
    
    result = []
    for plan in plans:
        import json
        features = json.loads(plan.features_json) if isinstance(plan.features_json, str) else plan.features_json
        
        result.append({
            'id': plan.id,
            'name': plan.name,
            'description': plan.description,
            'price': plan.price,
            'billing_cycle': plan.billing_cycle,
            'features': features
        })
    
    return jsonify(result), 200

@subscriptions_bp.route('/subscriptions', methods=['POST'])
@token_required
def create_subscription(current_user):
    """Create a new subscription for the current user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided!'}), 400
    
    # Validate required fields
    required_fields = ['plan_id', 'payment_method_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Check if plan exists
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
    
    # TODO: Integrate with Stripe for actual payment processing
    # For now, we'll simulate a successful payment
    
    # Create new subscription
    new_subscription = Subscription(
        user_id=current_user.id,
        plan_id=data['plan_id'],
        status='active',
        payment_method_id=data['payment_method_id'],
        stripe_subscription_id='sim_' + datetime.utcnow().strftime('%Y%m%d%H%M%S')
    )
    
    # Set end date based on billing cycle
    if plan.billing_cycle == 'monthly':
        new_subscription.end_date = datetime.utcnow().replace(month=datetime.utcnow().month + 1)
    elif plan.billing_cycle == 'yearly':
        new_subscription.end_date = datetime.utcnow().replace(year=datetime.utcnow().year + 1)
    
    db.session.add(new_subscription)
    db.session.commit()
    
    return jsonify({
        'message': 'Subscription created successfully!',
        'id': new_subscription.id,
        'status': new_subscription.status,
        'start_date': new_subscription.start_date.isoformat(),
        'end_date': new_subscription.end_date.isoformat() if new_subscription.end_date else None
    }), 201

@subscriptions_bp.route('/subscriptions/current', methods=['GET'])
@token_required
def get_current_subscription(current_user):
    """Get the current user's active subscription"""
    subscription = Subscription.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).first()
    
    if not subscription:
        return jsonify({'message': 'No active subscription found!'}), 404
    
    plan = Plan.query.get(subscription.plan_id)
    if not plan:
        return jsonify({'message': 'Subscription plan not found!'}), 500
    
    import json
    features = json.loads(plan.features_json) if isinstance(plan.features_json, str) else plan.features_json
    
    result = {
        'id': subscription.id,
        'status': subscription.status,
        'start_date': subscription.start_date.isoformat(),
        'end_date': subscription.end_date.isoformat() if subscription.end_date else None,
        'plan': {
            'id': plan.id,
            'name': plan.name,
            'description': plan.description,
            'price': plan.price,
            'billing_cycle': plan.billing_cycle,
            'features': features
        }
    }
    
    return jsonify(result), 200

@subscriptions_bp.route('/subscriptions/current', methods=['PUT'])
@token_required
def update_subscription(current_user):
    """Update the current user's subscription (e.g., change plan)"""
    subscription = Subscription.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).first()
    
    if not subscription:
        return jsonify({'message': 'No active subscription found!'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided!'}), 400
    
    if 'plan_id' in data:
        # Check if plan exists
        new_plan = Plan.query.get(data['plan_id'])
        if not new_plan:
            return jsonify({'message': 'Plan not found!'}), 404
        
        if not new_plan.is_active:
            return jsonify({'message': 'This plan is no longer available!'}), 400
        
        # TODO: Integrate with Stripe for actual plan change
        # For now, we'll simulate a successful plan change
        
        subscription.plan_id = data['plan_id']
        
        # Update end date based on new plan's billing cycle
        if new_plan.billing_cycle == 'monthly':
            subscription.end_date = datetime.utcnow().replace(month=datetime.utcnow().month + 1)
        elif new_plan.billing_cycle == 'yearly':
            subscription.end_date = datetime.utcnow().replace(year=datetime.utcnow().year + 1)
    
    db.session.commit()
    
    return jsonify({'message': 'Subscription updated successfully!'}), 200

@subscriptions_bp.route('/subscriptions/current', methods=['DELETE'])
@token_required
def cancel_subscription(current_user):
    """Cancel the current user's subscription"""
    subscription = Subscription.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).first()
    
    if not subscription:
        return jsonify({'message': 'No active subscription found!'}), 404
    
    # TODO: Integrate with Stripe for actual subscription cancellation
    # For now, we'll simulate a successful cancellation
    
    subscription.status = 'canceled'
    db.session.commit()
    
    return jsonify({'message': 'Subscription canceled successfully!'}), 200
