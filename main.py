import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, jsonify, request
from flask_cors import CORS
from src.models import db
from src.routes.auth import auth_bp
from src.routes.users import users_bp
from src.routes.content import content_bp
from src.routes.subscriptions import subscriptions_bp
from src.routes.payment import payment_bp
import os

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Configure database
    # For deployment, use SQLite instead of MySQL to avoid dependency issues
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketing_platform.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(content_bp, url_prefix='/api/content')
    app.register_blueprint(subscriptions_bp, url_prefix='/api/subscriptions')
    app.register_blueprint(payment_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return jsonify({
            "status": "success",
            "message": "Marketing Platform API is running",
            "version": "1.0.0"
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
    
    return app

# For local development
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

# For production deployment
app = create_app()
