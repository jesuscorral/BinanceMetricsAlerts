import threading

from services.rsi_service import *

# Parameters
available_symbols = ["DOGE/USDC", "ADA/USDC","ETH/USDC", "BTC/USDC", "XRP/USDC", "LTC/USDC"]
db_file = "rsi.db"
table_name = "rsi_data"

timeframe = '1d'
period = 6

frequency = 900 # loop frequency in seconds 300

# Create a connection to the SQLite database
conn = create_connection(db_file)
create_table_if_not_exists(conn, table_name)

# Start the RSI monitoring in a separate thread
rsi_thread = threading.Thread(target=monitor_rsi(symbols=available_symbols, period=period, frequency=frequency, conn=conn, timeframe=timeframe, table_name=table_name))
rsi_thread.daemon = True
rsi_thread.start()

