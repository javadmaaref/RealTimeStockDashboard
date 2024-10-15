# app/models.py
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """Model representing a user of the application"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    stocks = db.relationship('Stock', backref='user', lazy=True)  # Relationship with Stock model

class Stock(db.Model):
    """Model representing a stock being tracked by a user"""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    alert_price = db.Column(db.Float)  # Price at which an alert will be triggered
