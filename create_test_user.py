from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(username='testuser').first():
        u = User(username='testuser', email='test@example.com', password_hash=generate_password_hash('password123'))
        db.session.add(u)
        db.session.commit()
        print("User created.")
    else:
        print("User already exists.")
