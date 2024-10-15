# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, login_required, logout_user
from app.services.user_service import UserService

# Blueprint for authentication routes
bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration via POST request, serves registration form via GET"""

    # Handle form submission for registration
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        email = request.form.get('email')

        # Validate form data
        if not username or not password or not email:
            return jsonify({'error': 'All fields (username, password, email) are required'}), 400

        # Check if the username is already taken
        if UserService.get_user_by_username(username):
            return jsonify({'error': 'Username already exists'}), 400

        # Create new user
        UserService.create_user(username, password, phone, email)
        return jsonify({'message': 'User registered successfully'}), 201

    # Serve registration form if request method is GET
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login via POST request, serves login form via GET"""

    # Handle form submission for login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate form data
        if not username or not password:
            return jsonify({'error': 'Both username and password are required'}), 400

        # Check if user exists and the password is correct
        user = UserService.get_user_by_username(username)
        if user and UserService.check_password(user, password):
            # Log the user in
            login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 200

        # Provide more specific error message while avoiding too much detail for security
        return jsonify({'error': 'Invalid username or password'}), 401

    # Serve login form if request method is GET
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    """Logs out the current user"""

    # Log the user out
    logout_user()

    # Confirm logout success
    return jsonify({'message': 'Logged out successfully'}), 200
