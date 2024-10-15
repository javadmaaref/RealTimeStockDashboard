# app/__init__.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Set the login view

def create_app(config_class=Config):
    """Factory function to create the Flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize app extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Load user for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID"""
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import auth_routes, stock_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(stock_routes.bp)

    # Define the index route
    @app.route('/')
    def index():
        """Render the index page"""
        return render_template('index.html')

    return app
