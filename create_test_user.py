from app import app, db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    # Create test user
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(
        full_name='Test User',
        email='test@example.com',
        password=password_hash,
        farm_name='Test Farm',
        role='user',
        is_active=True
    )
    db.session.add(new_user)
    db.session.commit()
    print('✓ Test user created!')
    print('  Email: test@example.com')
    print('  Password: password123')
