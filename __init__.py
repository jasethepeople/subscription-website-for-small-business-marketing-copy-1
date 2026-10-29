# Database Models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Create a single SQLAlchemy instance to be used throughout the application
db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
def init_models():
    # These imports are placed here to avoid circular imports
    from src.models.user import User, BusinessProfile
    from src.models.subscription import Plan, Subscription
    from src.models.content import ContentItem, Template
    
    return {
        'User': User,
        'BusinessProfile': BusinessProfile,
        'Plan': Plan,
        'Subscription': Subscription,
        'ContentItem': ContentItem,
        'Template': Template
    }
