# app/services/user_service.py
from app import db, bcrypt
from app.models import User

class UserService:
    """Service class for managing user-related operations"""

    @staticmethod
    def create_user(username, password, phone, email):
        """Creates a new user with a hashed password and saves them to the database"""
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, phone=phone, email=email)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_username(username):
        """Fetches a user from the database by username"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def check_password(user, password):
        """Checks if the provided password matches the stored hashed password"""
        return bcrypt.check_password_hash(user.password, password)
