from flask import Blueprint, request, jsonify
from functools import wraps

from src.routes.auth import token_required
from src.models.user import db, User, BusinessProfile

users_bp = Blueprint('users', __name__)

@users_bp.route('/me', methods=['GET'])
@token_required
def get_user_profile(current_user):
    """Get the current user's profile information"""
    user_data = {
        'id': current_user.id,
        'email': current_user.email,
        'name': current_user.name,
        'created_at': current_user.created_at.isoformat(),
        'last_login': current_user.last_login.isoformat() if current_user.last_login else None
    }
    
    # Include business profile if it exists
    if current_user.business_profile:
        business_profile = current_user.business_profile
        user_data['business_profile'] = {
            'id': business_profile.id,
            'business_name': business_profile.business_name,
            'industry': business_profile.industry,
            'description': business_profile.description,
            'logo_url': business_profile.logo_url,
            'brand_colors': business_profile.brand_colors,
            'website': business_profile.website
        }
    
    return jsonify(user_data), 200

@users_bp.route('/me', methods=['PUT'])
@token_required
def update_user_profile(current_user):
    """Update the current user's profile information"""
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided!'}), 400
    
    # Update user fields if provided
    if 'name' in data:
        current_user.name = data['name']
    
    if 'email' in data:
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != current_user.id:
            return jsonify({'message': 'Email already in use!'}), 409
        current_user.email = data['email']
    
    db.session.commit()
    
    return jsonify({'message': 'User profile updated successfully!'}), 200

@users_bp.route('/me/business', methods=['GET'])
@token_required
def get_business_profile(current_user):
    """Get the current user's business profile"""
    if not current_user.business_profile:
        return jsonify({'message': 'Business profile not found!'}), 404
    
    business_profile = current_user.business_profile
    profile_data = {
        'id': business_profile.id,
        'business_name': business_profile.business_name,
        'industry': business_profile.industry,
        'description': business_profile.description,
        'logo_url': business_profile.logo_url,
        'brand_colors': business_profile.brand_colors,
        'website': business_profile.website,
        'created_at': business_profile.created_at.isoformat(),
        'updated_at': business_profile.updated_at.isoformat()
    }
    
    return jsonify(profile_data), 200

@users_bp.route('/me/business', methods=['POST', 'PUT'])
@token_required
def create_or_update_business_profile(current_user):
    """Create or update the current user's business profile"""
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided!'}), 400
    
    # Validate required fields for creation
    if request.method == 'POST' and not current_user.business_profile:
        required_fields = ['business_name', 'industry']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Create or update business profile
    if current_user.business_profile:
        # Update existing profile
        business_profile = current_user.business_profile
        status_code = 200
        message = 'Business profile updated successfully!'
    else:
        # Create new profile
        business_profile = BusinessProfile(user_id=current_user.id)
        db.session.add(business_profile)
        status_code = 201
        message = 'Business profile created successfully!'
    
    # Update fields if provided
    if 'business_name' in data:
        business_profile.business_name = data['business_name']
    
    if 'industry' in data:
        business_profile.industry = data['industry']
    
    if 'description' in data:
        business_profile.description = data['description']
    
    if 'logo_url' in data:
        business_profile.logo_url = data['logo_url']
    
    if 'brand_colors' in data:
        business_profile.brand_colors = data['brand_colors']
    
    if 'website' in data:
        business_profile.website = data['website']
    
    db.session.commit()
    
    return jsonify({'message': message, 'id': business_profile.id}), status_code
