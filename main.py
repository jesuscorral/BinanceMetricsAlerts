from binance.client import Client
import threading

from rsi_service import *
from draw_chart import *
from database_service import *
from binance_service import *

# Parameters
available_symbols = ["DOGE/USDT", "ADA/USDT","ETH/USDT", "BTC/USDT", "XRP/USDT", "LTC/USDT"]

timeframe = '1d'
database_name = "rsi.db"
period = 6
table_name = "rsi_data"

frequency = 300 # loop frequency in seconds 300

# Create a connection to the SQLite database
conn = create_connection(database_name)
create_table_if_not_exists(conn, table_name)

# Start the RSI monitoring in a separate thread
rsi_thread = threading.Thread(target=monitor_rsi(symbols=available_symbols, period=period, frequency=frequency, conn=conn, timeframe=timeframe, table_name=table_name))
rsi_thread.daemon = True
rsi_thread.start()

