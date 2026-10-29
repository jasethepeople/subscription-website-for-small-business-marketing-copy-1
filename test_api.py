import pytest
from src.main import create_app, db
from werkzeug.security import generate_password_hash
import json
from datetime import datetime, timedelta

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Set the testing configuration
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test_secret_key'
    })
    
    # Create the database and the database tables
    with app.app_context():
        db.create_all()
        
        # Create test data
        seed_test_data()
        
    yield app
    
    # Clean up
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def seed_test_data():
    """Seed the database with test data."""
    # Import models here to avoid circular imports
    from src.models.user import User, BusinessProfile
    from src.models.subscription import Plan, Subscription
    from src.models.content import ContentItem, Template
    
    # Create test plans
    basic_plan = Plan(
        name="Basic Test",
        description="Basic test plan",
        price=9.99,
        billing_cycle="monthly",
        features_json=json.dumps({
            "content_generation": 10,
            "social_platforms": ["facebook", "instagram"],
            "templates": "basic",
            "ai_assistance": False
        })
    )
    
    premium_plan = Plan(
        name="Premium Test",
        description="Premium test plan",
        price=29.99,
        billing_cycle="monthly",
        features_json=json.dumps({
            "content_generation": 50,
            "social_platforms": ["facebook", "instagram", "twitter", "linkedin"],
            "templates": "premium",
            "ai_assistance": True
        })
    )
    
    db.session.add_all([basic_plan, premium_plan])
    
    # Create test user
    test_user = User(
        email="test@example.com",
        password_hash=generate_password_hash("password123"),
        name="Test User"
    )
    db.session.add(test_user)
    db.session.commit()
    
    # Create test business profile
    test_profile = BusinessProfile(
        user_id=test_user.id,
        business_name="Test Business",
        industry="Technology",
        description="A test business for testing purposes",
        website="https://testbusiness.com"
    )
    db.session.add(test_profile)
    
    # Create test subscription
    test_subscription = Subscription(
        user_id=test_user.id,
        plan_id=basic_plan.id,
        status="active",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30),
        payment_method_id="test_payment_method",
        stripe_subscription_id="test_stripe_subscription"
    )
    db.session.add(test_subscription)
    
    # Create test templates
    test_template = Template(
        category="social",
        name="Test Template",
        description="A test template",
        structure_json={
            "template_type": "test",
            "fields": [
                {
                    "name": "headline",
                    "type": "text",
                    "max_length": 100,
                    "placeholder": "Test Headline"
                },
                {
                    "name": "content",
                    "type": "textarea",
                    "max_length": 500,
                    "placeholder": "Test Content"
                }
            ],
            "platforms": ["facebook", "instagram"]
        },
        thumbnail_url="/static/templates/thumbnails/test.jpg",
        is_premium=False
    )
    db.session.add(test_template)
    
    # Create test content item
    test_content = ContentItem(
        user_id=test_user.id,
        type="social",
        platform="facebook",
        content_text="This is a test content item",
        status="draft",
        template_id=test_template.id
    )
    db.session.add(test_content)
    
    db.session.commit()

def get_auth_token(client):
    """Helper function to get an authentication token."""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    return json.loads(response.data)['token']

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_user_registration(client):
    """Test user registration."""
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'newpassword123',
        'name': 'New User'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user_id' in data
    assert data['message'] == 'User registered successfully!'

def test_user_login(client):
    """Test user login."""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert data['user']['email'] == 'test@example.com'

def test_get_user_profile(client):
    """Test getting user profile."""
    token = get_auth_token(client)
    response = client.get('/api/users/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'test@example.com'
    assert 'business_profile' in data
    assert data['business_profile']['business_name'] == 'Test Business'

def test_get_plans(client):
    """Test getting subscription plans."""
    response = client.get('/api/plans')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == 'Basic Test'
    assert data[1]['name'] == 'Premium Test'

def test_get_templates(client):
    """Test getting content templates."""
    token = get_auth_token(client)
    response = client.get('/api/templates', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Template'
    assert data[0]['category'] == 'social'

def test_create_content(client):
    """Test creating content."""
    token = get_auth_token(client)
    response = client.post('/api/content', json={
        'type': 'social',
        'platform': 'instagram',
        'content_text': 'New test content',
        'status': 'draft'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Content created successfully!'
    assert 'id' in data

def test_get_content(client):
    """Test getting content items."""
    token = get_auth_token(client)
    response = client.get('/api/content', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['content_text'] == 'This is a test content item'
    assert data[0]['type'] == 'social'

def test_get_current_subscription(client):
    """Test getting current subscription."""
    token = get_auth_token(client)
    response = client.get('/api/subscriptions/current', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'active'
    assert data['plan']['name'] == 'Basic Test'
