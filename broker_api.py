# broker_api.py
import MetaTrader5 as mt5
import pandas as pd
import logging

class BrokerAPI:
    def __init__(self, account, password, server):
        self.account = account
        self.password = password
        self.server = server

        # Initialize MT5
        if not mt5.initialize():
            logging.error("Failed to initialize MT5")
            raise Exception("Failed to initialize MT5")

        # Log in to the account
        authorized = mt5.login(self.account, self.password, self.server)
        if not authorized:
            logging.error(f"Failed to log in to account #{self.account}")
            raise Exception(f"Failed to log in: {mt5.last_error()}")

    def get_market_data(self, symbol, timeframe):
        """Fetch historical market data for the specified symbol and timeframe."""
        try:
            # Map timeframe to MT5 timeframe
            mt5_timeframe = {
                "1h": mt5.TIMEFRAME_H1,
                "1D": mt5.TIMEFRAME_D1,
                "1M": mt5.TIMEFRAME_M1,
            }.get(timeframe, mt5.TIMEFRAME_H1)

            # Fetch historical data
            bars = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, 100)  # Last 100 bars
            if bars is None:
                logging.error(f"Failed to fetch market data for {symbol}")
                return None

            # Convert to DataFrame
            df = pd.DataFrame(bars)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        except Exception as e:
            logging.error(f"Error fetching market data: {e}")
            return None

    def place_order(self, symbol, side, quantity, stop_loss, take_profit):
        """Place a trade order."""
        try:
            # Map side to MT5 order type
            order_type = mt5.ORDER_TYPE_BUY if side == "buy" else mt5.ORDER_TYPE_SELL

            # Get the current price
            price = mt5.symbol_info_tick(symbol).ask if side == "buy" else mt5.symbol_info_tick(symbol).bid

            # Prepare the order request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": quantity,
                "type": order_type,
                "price": price,
                "sl": stop_loss,
                "tp": take_profit,
                "deviation": 10,
                "magic": 234000,
                "comment": "Python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # Send the order
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logging.error(f"Failed to place order: {result.comment}")
                return None

            logging.info(f"Order placed successfully. Order ID: {result.order}")
            return result
        except Exception as e:
            logging.error(f"Error placing order: {e}")
            return None