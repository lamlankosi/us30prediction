# main.py
import logging
import time
import pandas as pd
from broker_api import BrokerAPI
from strategy import TradingStrategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("forex_bot.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

# Initialize broker API and trading strategy
broker = BrokerAPI(account=208543245, password="@Lamlankosi7", server="Exness-MT5Trial9")
strategy = TradingStrategy(short_window=10, long_window=50, risk_per_trade=0.01)

def main():
    logging.info("Forex trading bot started.")

    # Input account balance and timeframe
    balance = float(input("Enter your account balance: "))
    timeframe = input("Enter the timeframe (e.g., 1M, 1h, 1D): ")

    while True:
        try:
            # Fetch market data for the specified timeframe
            data = broker.get_market_data("US30m", timeframe)
            if data is None:
                logging.warning("No market data received. Retrying...")
                time.sleep(60)
                continue

            # Analyze data and generate signal
            analyzed_data = strategy.analyze(data)
            signal = strategy.generate_signal(analyzed_data, balance, timeframe)

            # Log the signal
            logging.info(f"Generated signal: {signal}")

            # Wait before next iteration
            if timeframe == "1M":
                time.sleep(60)  # Sleep for 1 minute
            elif timeframe == "1h":
                time.sleep(3600)  # Sleep for 1 hour
            elif timeframe == "1D":
                time.sleep(86400)  # Sleep for 1 day
            else:
                time.sleep(3600)  # Default sleep for 1 hour
        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()