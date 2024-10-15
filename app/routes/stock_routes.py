# app/routes/stock_routes.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.stock_service import StockService, YahooFinanceService
from app.services.notification_service import NotificationService
from app.models import Stock
from app import db

# Blueprint for stock-related routes
bp = Blueprint('stocks', __name__)

# Instantiate services
stock_service = StockService(YahooFinanceService())
notification_service = NotificationService()


# Fetch stock data for a given symbol
@bp.route('/api/stock/<symbol>')
def stock_data(symbol):
    """Fetches real-time stock data for the given symbol"""

    # Attempt to fetch stock data
    result = stock_service.get_stock_data(symbol)

    # If data can't be fetched, return an error
    if not result:
        return jsonify({'error': 'Unable to fetch stock data'}), 400

    # If the user is logged in, check if any price alerts need to be sent
    if current_user.is_authenticated:
        stock = Stock.query.filter_by(user_id=current_user.id, symbol=symbol).first()

        # If the user has set an alert price for the stock, and the stock price is below that alert, notify the user
        if stock and stock.alert_price:
            if result['price'] <= stock.alert_price:
                message = f"Alert: {symbol} has reached or fallen below ${stock.alert_price}"

                # Send SMS alert if user has provided a phone number
                if current_user.phone:
                    notification_service.notify('sms', current_user.phone, message)

                # Send email alert if user has provided an email address
                if current_user.email:
                    notification_service.notify('email', current_user.email, message)

    # Return the fetched stock data as a JSON response
    return jsonify(result)


# Fetch historical data for a given stock symbol
@bp.route('/api/historical/<symbol>')
def historical_data(symbol):
    """Fetches historical stock data for the given symbol"""

    # Fetch historical data
    data = stock_service.get_historical_data(symbol)

    # Log the data for debugging
    print('Historical data:', data)

    # If no data is returned, respond with an error
    if not data:
        return jsonify({'error': 'Unable to fetch historical data'}), 400

    # Return the historical data as JSON
    return jsonify(data)


# Manage the user's stock watchlist
@bp.route('/watchlist', methods=['GET', 'POST'])
@login_required
def watchlist():
    """Allows users to view and modify their stock watchlist"""

    # If the request is POST, add a new stock to the watchlist
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        alert_price = request.form.get('alert_price')

        # Create a new stock entry for the user's watchlist
        stock = Stock(symbol=symbol, user_id=current_user.id, alert_price=alert_price)
        db.session.add(stock)
        db.session.commit()

        # Notify the user that the stock has been added to the watchlist
        return jsonify({'message': 'Stock added to watchlist'}), 201

    # If the request is GET, retrieve and return the user's watchlist
    stocks = Stock.query.filter_by(user_id=current_user.id).all()
    watchlist_data = [{'symbol': stock.symbol, 'alert_price': stock.alert_price} for stock in stocks]

    # Return the watchlist as JSON
    return jsonify(watchlist_data)
