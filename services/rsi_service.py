import pandas as pd
from datetime import datetime, timezone
import time

from services.database_service import *
from services.binance_service import *
from services.notifications import *

def rsi_calc(ohlc: pd.DataFrame, period: int):
    delta = ohlc['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def monitor_rsi(symbols, period, frequency, conn, timeframe, table_name):
    while True:
        for symbol in symbols:
            df = fetch_binance_data(symbol, timeframe)
            rsi_6 = rsi_calc(df, period)
            rsi_6_value = rsi_6.iloc[-1]
            current_time = datetime.now(timezone.utc)
            utc_timestamp = current_time.timestamp()
            current_price = fetch_current_price(symbol)

            print(f"rsi: {rsi_6_value}, symbol: {symbol}, price: {current_price}, timestamp: {utc_timestamp}")
            insert_data(conn, rsi_6_value, utc_timestamp, symbol, table_name)
            check_conditions_to_send_notification(rsi_6_value, symbol, current_price, timeframe)
        time.sleep(frequency)  # Sleep for 'frequency' seconds