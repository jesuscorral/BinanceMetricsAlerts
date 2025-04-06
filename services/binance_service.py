import ccxt
import pandas as pd
import os
from binance.client import Client

def fetch_binance_data(symbol, timeframe, limit=1000):
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime
    return df

def fetch_current_price(symbol):
    binance = ccxt.binance()
    ticker = binance.fetch_ticker(symbol)
    current_price = ticker['last']
    return current_price

def get_open_orders():
    client = get_binance_client()
    try:
        open_orders = client.get_open_orders()
        for order in open_orders:
            print(f"Symbol: {order['symbol']}, Order ID: {order['orderId']}, Status: {order['status']}")
        return open_orders
    except Exception as e:
        print(f"Error fetching open orders: {e}")
        return []


def get_symbol_balance(asset):
    client = get_binance_client()
    try:
        balance = client.get_asset_balance(asset=asset)
        if balance:
            return float(balance['free'])
        else:
            print(f"No balance found for {asset}")
            return 0.0
    except Exception as e:
        print(f"Error fetching balance for {asset}: {e}")
        return 0.0

def get_binance_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    client = Client(api_key, api_secret)
    return client  