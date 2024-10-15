# app/services/stock_service.py
import yfinance as yf
import pandas as pd
from abc import ABC, abstractmethod


class StockDataSource(ABC):
    """Abstract base class for stock data sources"""

    @abstractmethod
    def get_stock_data(self, symbol):
        """Fetches the latest stock data for a given symbol"""
        pass

    @abstractmethod
    def get_historical_data(self, symbol):
        """Fetches the historical stock data for a given symbol"""
        pass


class YahooFinanceService(StockDataSource):
    """Concrete implementation of StockDataSource using Yahoo Finance"""

    def get_stock_data(self, symbol):
        """Fetches the latest stock data from Yahoo Finance for the given symbol"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            if data.empty:
                return None
            latest_data = data.iloc[-1]
            return {
                'symbol': symbol,
                'datetime': latest_data.name.strftime('%Y-%m-%d %H:%M:%S'),
                'price': latest_data['Close']
            }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def get_historical_data(self, symbol):
        """Fetches the historical stock data for the last year from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1y")
            data.reset_index(inplace=True)
            return data[['Date', 'Close']].rename(columns={'Date': 'datetime', 'Close': 'price'}).to_dict(
                orient='records')
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None


class StockService:
    """Service class to handle stock data operations"""

    def __init__(self, stock_data_source: StockDataSource):
        """Initialize the service with a data source"""
        self.stock_data_source = stock_data_source

    def get_stock_data(self, symbol):
        """Fetches the latest stock data for a symbol"""
        return self.stock_data_source.get_stock_data(symbol)

    def get_historical_data(self, symbol):
        """Fetches the historical stock data for a symbol"""
        return self.stock_data_source.get_historical_data(symbol)

    def calculate_technical_indicators(self, data):
        """Calculates technical indicators (SMA, RSI, Bollinger Bands) for given stock data"""
        df = pd.DataFrame(data).T
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        # Simple Moving Average (SMA)
        df['SMA20'] = df['close'].rolling(window=20).mean()

        # Relative Strength Index (RSI)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # Bollinger Bands (BB)
        df['BB_middle'] = df['close'].rolling(window=20).mean()
        df['BB_upper'] = df['BB_middle'] + 2 * df['close'].rolling(window=20).std()
        df['BB_lower'] = df['BB_middle'] - 2 * df['close'].rolling(window=20).std()

        # Return the last 30 days of data with indicators
        return df.tail(30).to_dict(orient='index')
