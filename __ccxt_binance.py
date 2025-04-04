import ccxt
import pandas as pd

def fetch_binance_data(symbol, timeframe, limit=1000):
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime
    return df

def rsi_calc(ohlc: pd.DataFrame, period: int):
    delta = ohlc['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def stoch_rsi_calc(rsi: pd.Series, stoch_period=14, k_period=3, d_period=3):
    min_rsi = rsi.rolling(window=stoch_period).min()
    max_rsi = rsi.rolling(window=stoch_period).max()
    stoch_rsi = (rsi - min_rsi) / (max_rsi - min_rsi) * 100

    K = stoch_rsi.rolling(window=k_period).mean()
    D = K.rolling(window=d_period).mean()

    return K, D

def rsi_and_stoch_rsi(symbol, timeframe):
    df = fetch_binance_data(symbol, timeframe)

    rsi_6 = rsi_calc(df, 6)
    rsi_7 = rsi_calc(df, 7)
    rsi_21 = rsi_calc(df, 21)

    rsi_6_value = rsi_6.iloc[-1]
    rsi_7_value = rsi_7.iloc[-1]
    rsi_21_value = rsi_21.iloc[-1]

    stoch_rsi_k, stoch_rsi_d = stoch_rsi_calc(rsi_7, 14, 3, 3)
    stoch_rsi_k_value = stoch_rsi_k.iloc[-1]
    stoch_rsi_d_value = stoch_rsi_d.iloc[-1]

    return rsi_6_value, rsi_7_value, rsi_21_value, stoch_rsi_k_value, stoch_rsi_d_value

# Parameters
symbol = 'LTC/USDT'
timeframe = '1h'

# Get RSI and Stoch RSI values
rsi_6_value, rsi_7_value, rsi_21_value, stoch_rsi_k_value, stoch_rsi_d_value = rsi_and_stoch_rsi(symbol, timeframe)

# Print results
print(f"RSI 6: {rsi_6_value:.4f}")
print(f"RSI 7: {rsi_7_value:.4f}")
print(f"RSI 21: {rsi_21_value:.4f}")
print(f"Stochastic RSI K: {stoch_rsi_k_value:.4f}")
print(f"Stochastic RSI D: {stoch_rsi_d_value:.4f}")