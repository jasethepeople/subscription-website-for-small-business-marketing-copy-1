from flask import Blueprint, request, jsonify
from datetime import datetime

from src.routes.auth import token_required
from src.models.content import db, ContentItem, Template
from src.models.subscription import Subscription, Plan

content_bp = Blueprint('content', __name__)

@content_bp.route('/templates', methods=['GET'])
@token_required
def get_templates(current_user):
    """Get all available templates, filtered by category if specified"""
    category = request.args.get('category')
    is_premium = request.args.get('is_premium')
    
    # Start with base query
    query = Template.query
    
    # Apply filters if provided
    if category:
        query = query.filter_by(category=category)
    
    if is_premium is not None:
        is_premium_bool = is_premium.lower() == 'true'
        query = query.filter_by(is_premium=is_premium_bool)
    
    templates = query.all()
    
    result = []
    for template in templates:
        result.append({
            'id': template.id,
            'category': template.category,
            'name': template.name,
            'description': template.description,
            'thumbnail_url': template.thumbnail_url,
            'is_premium': template.is_premium,
            'created_at': template.created_at.isoformat()
        })
    
    return jsonify(result), 200

@content_bp.route('/templates/<template_id>', methods=['GET'])
@token_required
def get_template(current_user, template_id):
    """Get a specific template by ID"""
    template = Template.query.get(template_id)
    
    if not template:
        return jsonify({'message': 'Template not found!'}), 404
    
    # Check if user has access to premium templates
    if template.is_premium:
        # Get user's active subscription
        subscription = Subscription.query.filter_by(
            user_id=current_user.id, 
            status='active'
        ).first()
        
        if not subscription:
            return jsonify({'message': 'Premium template requires an active subscription!'}), 403
        
        # Check if subscription plan includes premium templates
        plan = Plan.query.get(subscription.plan_id)
        if not plan:
            return jsonify({'message': 'Subscription plan not found!'}), 500
        
        import json
        features = json.loads(plan.features_json)
        if features.get('templates') not in ['premium', 'all']:
            return jsonify({'message': 'Your subscription plan does not include premium templates!'}), 403
    
    result = {
        'id': template.id,
        'category': template.category,
        'name': template.name,
        'description': template.description,
        'structure_json': template.structure_json,
        'thumbnail_url': template.thumbnail_url,
        'is_premium': template.is_premium,
        'created_at': template.created_at.isoformat(),
        'updated_at': template.updated_at.isoformat()
    }
    
    return jsonify(result), 200

@content_bp.route('/content', methods=['POST'])
@token_required
def create_content(current_user):
    """Create a new content item"""
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided!'}), 400
    
    # Validate required fields
    required_fields = ['type']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Check if user has an active subscription
    subscription = Subscription.query.filter_by(
        user_id=current_user.id, 
        status='active'
    ).first()
    
    if not subscription:
        return jsonify({'message': 'Active subscription required to create content!'}), 403
    
    # Create new content item
    new_content = ContentItem(
        user_id=current_user.id,
        type=data['type'],
        platform=data.get('platform'),
        content_text=data.get('content_text'),
        media_urls=data.get('media_urls'),
        status='draft',
        template_id=data.get('template_id')
    )
    
    # Handle scheduling if provided
    if 'scheduled_for' in data:
        try:
            scheduled_for = datetime.fromisoformat(data['scheduled_for'])
            new_content.scheduled_for = scheduled_for
            new_content.status = 'scheduled'
        except ValueError:
            return jsonify({'message': 'Invalid date format for scheduled_for!'}), 400
    
    db.session.add(new_content)
    db.session.commit()
    
    return jsonify({
        'message': 'Content created successfully!',
        'id': new_content.id,
        'status': new_content.status
    }), 201

@content_bp.route('/content', methods=['GET'])
@token_required
def get_content_items(current_user):
    """Get all content items for the current user"""
    # Get query parameters for filtering
    content_type = request.args.get('type')
    status = request.args.get('status')
    platform = request.args.get('platform')
    
    # Start with base query
    query = ContentItem.query.filter_by(user_id=current_user.id)
    
    # Apply filters if provided
    if content_type:
        query = query.filter_by(type=content_type)
    
    if status:
        query = query.filter_by(status=status)
    
    if platform:
        query = query.filter_by(platform=platform)
    
    # Order by created_at descending (newest first)
    query = query.order_by(ContentItem.created_at.desc())
    
    content_items = query.all()
    
    result = []
    for item in content_items:
        result.append({
            'id': item.id,
            'type': item.type,
            'platform': item.platform,
            'content_text': item.content_text,
            'media_urls': item.media_urls,
            'status': item.status,
            'created_at': item.created_at.isoformat(),
            'scheduled_for': item.scheduled_for.isoformat() if item.scheduled_for else None,
            'published_at': item.published_at.isoformat() if item.published_at else None,
            'template_id': item.template_id
        })
    
    return jsonify(result), 200

@content_bp.route('/content/<content_id>', methods=['GET'])
@token_required
def get_content_item(current_user, content_id):
    """Get a specific content item by ID"""
    content_item = ContentItem.query.filter_by(id=content_id, user_id=current_user.id).first()
    
    if not content_item:
        return jsonify({'message': 'Content item not found!'}), 404
    
    result = {
        'id': content_item.id,
        'type': content_item.type,
        'platform': content_item.platform,
        'content_text': content_item.content_text,
        'media_urls': content_item.media_urls,
        'status': content_item.status,
        'created_at': content_item.created_at.isoformat(),
        'scheduled_for': content_item.scheduled_for.isoformat() if content_item.scheduled_for else None,
        'published_at': content_item.published_at.isoformat() if content_item.published_at else None,
        'template_id': content_item.template_id
    }
    
    # Include template data if available
    if content_item.template:
        result['template'] = {
            'id': content_item.template.id,
            'name': content_item.template.name,
            'category': content_item.template.category,
            'structure_json': content_item.template.structure_json
        }
    
    return jsonify(result), 200

@content_bp.route('/content/<content_id>', methods=['PUT'])
@token_required
def update_content_item(current_user, content_id):
    """Update a specific content item"""
    content_item = ContentItem.query.filter_by(id=content_id, user_id=current_user.id).first()
    
    if not content_item:
        return jsonify({'message': 'Content item not found!'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided!'}), 400
    
    # Update fields if provided
    if 'type' in data:
        content_item.type = data['type']
    
    if 'platform' in data:
        content_item.platform = data['platform']
    
    if 'content_text' in data:
        content_item.content_text = data['content_text']
    
    if 'media_urls' in data:
        content_item.media_urls = data['media_urls']
    
    if 'status' in data:
        content_item.status = data['status']
    
    if 'scheduled_for' in data:
        if data['scheduled_for']:
            try:
                scheduled_for = datetime.fromisoformat(data['scheduled_for'])
                content_item.scheduled_for = scheduled_for
                if content_item.status == 'draft':
                    content_item.status = 'scheduled'
            except ValueError:
                return jsonify({'message': 'Invalid date format for scheduled_for!'}), 400
        else:
            content_item.scheduled_for = None
    
    db.session.commit()
    
    return jsonify({'message': 'Content item updated successfully!'}), 200

@content_bp.route('/content/<content_id>', methods=['DELETE'])
@token_required
def delete_content_item(current_user, content_id):
    """Delete a specific content item"""
    content_item = ContentItem.query.filter_by(id=content_id, user_id=current_user.id).first()
    
    if not content_item:
        return jsonify({'message': 'Content item not found!'}), 404
    
    db.session.delete(content_item)
    db.session.commit()
    
    return jsonify({'message': 'Content item deleted successfully!'}), 200

@content_bp.route('/content/<content_id>/publish', methods=['POST'])
@token_required
def publish_content_item(current_user, content_id):
    """Publish a content item"""
    content_item = ContentItem.query.filter_by(id=content_id, user_id=current_user.id).first()
    
    if not content_item:
        return jsonify({'message': 'Content item not found!'}), 404
    
    if content_item.status == 'published':
        return jsonify({'message': 'Content item is already published!'}), 400
    
    content_item.status = 'published'
    content_item.published_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Content item published successfully!'}), 200
