from TelegramBot.bot import *
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your bot token  chatand ID
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")


def check_rsi_threshold(rsi_6_value, symbol, current_price, timeframe):
    # Define your threshold values
    upper_threshold = 70
    lower_threshold = 40

    # Check if the RSI value crosses the thresholds
    if rsi_6_value > upper_threshold:
        message = f"HIGH RSI Alert: {symbol} - {upper_threshold}+. RSI {timeframe}: {rsi_6_value} \n Current Price: {current_price}"
        print(message)
        send_telegram_message(bot_token, chat_id, message)
    elif rsi_6_value < lower_threshold:
        message = f"LOW RSI Alert: {symbol} - {lower_threshold}-. RSI {timeframe}: {rsi_6_value} \n Current Price: {current_price}"
        print(message)
        send_telegram_message(bot_token, chat_id, message)
