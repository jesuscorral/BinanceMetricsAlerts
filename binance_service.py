import ccxt
import pandas as pd

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