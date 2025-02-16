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
# main.py
broker = BrokerAPI(account=208543245, password="@Lamlankosi7", server="Exness-MT5Trial9")
strategy = TradingStrategy(short_window=10, long_window=50)

def main():
    logging.info("Forex trading bot started.")
    while True:
        try:
            # Fetch market data
            data = broker.get_market_data("US30m", "1h")
            if data is None:
                logging.warning("No market data received. Retrying...")
                time.sleep(60)
                continue

            # Analyze data and generate signal
            analyzed_data = strategy.analyze(data)
            signal = strategy.generate_signal(analyzed_data)
            logging.info(f"Generated signal: {signal}")

            # Execute trade based on signal
            if signal == "buy":
                broker.place_order("US30m", "buy", 1.0, stop_loss=33000, take_profit=34000)
                logging.info("Placed a buy order.")
            elif signal == "sell":
                broker.place_order("US30m", "sell", 1.0, stop_loss=34000, take_profit=33000)
                logging.info("Placed a sell order.")

            # Wait before next iteration
            time.sleep(3600)  # Sleep for 1 hour
        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()