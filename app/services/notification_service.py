# app/services/notification_service.py
from abc import ABC, abstractmethod
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import Config

class NotificationStrategy(ABC):
    """Abstract base class for notification strategies"""
    @abstractmethod
    def send_notification(self, recipient, message):
        """Send a notification to the recipient"""
        pass

class SMSNotification(NotificationStrategy):
    """Concrete strategy for sending SMS notifications using Twilio"""
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

    def send_notification(self, recipient, message):
        """Send an SMS notification to the recipient"""
        self.client.messages.create(
            body=message,
            from_=Config.TWILIO_PHONE_NUMBER,
            to=recipient
        )

class EmailNotification(NotificationStrategy):
    """Concrete strategy for sending email notifications"""
    def send_notification(self, recipient, message):
        """Send an email notification to the recipient"""
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = "Stock Price Alert"
        msg.attach(MIMEText(message, 'plain'))

        # Send email using Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

class NotificationService:
    """Service class for managing and sending notifications"""
    def __init__(self):
        # Initialize with predefined strategies: SMS and Email
        self.strategies = {
            'sms': SMSNotification(),
            'email': EmailNotification()
        }

    def add_strategy(self, name, strategy):
        """Add a new notification strategy dynamically"""
        self.strategies[name] = strategy

    def notify(self, strategy_name, recipient, message):
        """Send a notification using the specified strategy"""
        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown notification strategy: {strategy_name}")
        self.strategies[strategy_name].send_notification(recipient, message)
