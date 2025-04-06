from TelegramBot.bot import *
from dotenv import load_dotenv
import os

from services.binance_service import *

load_dotenv()

# Replace with your bot token  chatand ID
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

def check_conditions_to_send_notification(rsi_6_value, symbol, current_price, timeframe):
    # Define your threshold values
    lower_threshold = 40
    upper_threshold = 70

    # Check if the RSI value crosses the thresholds
    if rsi_is_below_low_threshold(rsi_6_value, lower_threshold) and has_opened_position(symbol) == False and has_remaining_credit('USDC') == True:
        message = f"LOW RSI Alert: {symbol} - {lower_threshold}-. RSI {timeframe}: {rsi_6_value} \n Current Price: {current_price}"

        print(message)
        send_telegram_message(bot_token, chat_id, message)
    # elif rsi_is_above_upper_threshold(rsi_6_value, upper_threshold):
    # message = f"HIGH RSI Alert: {symbol} - {upper_threshold}+. RSI {timeframe}: {rsi_6_value} \n Current Price: {current_price}"
    #     print(message)
    #     send_telegram_message(bot_token, chat_id, message)

def rsi_is_below_low_threshold(rsi_value, lower_threshold):
    return rsi_value < lower_threshold


def rsi_is_above_upper_threshold(rsi_value, upper_threshold):
    return rsi_value > upper_threshold

def has_opened_position(symbol):
    symbol = symbol.replace("/", "").upper()
    open_orders = get_open_orders()
    
    ret = open_orders and any(symbol in order['symbol'] for order in open_orders)
    return ret

def has_remaining_credit(symbol):
    credit_threshold = 100 # 
    credit = get_symbol_balance(symbol)
    
    has_remaining_credit = credit is not None and credit >= credit_threshold
   
    return has_remaining_credit