# strategy.py
import pandas as pd
import numpy as np

class TradingStrategy:
    def __init__(self, short_window=10, long_window=50, risk_per_trade=0.01):
        self.short_window = short_window
        self.long_window = long_window
        self.risk_per_trade = risk_per_trade  # Risk 1% of account balance per trade

    def analyze(self, data):
        """Analyze market data and generate trading signals."""
        data['short_ma'] = data['close'].rolling(window=self.short_window).mean()
        data['long_ma'] = data['close'].rolling(window=self.long_window).mean()
        data['signal'] = np.where(data['short_ma'] > data['long_ma'], 1, -1)
        return data

    def generate_signal(self, data, balance, timeframe):
        """Generate a buy/sell signal with SL, TP, and position size."""
        latest_signal = data['signal'].iloc[-1]
        current_price = data['close'].iloc[-1]

        # Adjust SL/TP distances based on timeframe
        if timeframe == "1M":
            stop_loss_distance = 10  # 10 pips for 1-minute timeframe
            take_profit_distance = 20  # 20 pips for 1-minute timeframe
        elif timeframe == "1h":
            stop_loss_distance = 100  # 100 pips for 1-hour timeframe
            take_profit_distance = 200  # 200 pips for 1-hour timeframe
        elif timeframe == "1D":
            stop_loss_distance = 200  # 200 pips for 1-day timeframe
            take_profit_distance = 400  # 400 pips for 1-day timeframe
        else:
            stop_loss_distance = 100  # Default for other timeframes
            take_profit_distance = 200  # Default for other timeframes

        # Calculate position size based on risk management
        risk_amount = balance * self.risk_per_trade
        position_size = risk_amount / stop_loss_distance  # Simplified calculation

        # Generate signal
        if latest_signal == 1:
            signal = {
                "action": "buy",
                "price": current_price,
                "stop_loss": current_price - stop_loss_distance,
                "take_profit": current_price + take_profit_distance,
                "position_size": position_size,
                "timeframe": timeframe,  # Include timeframe in the signal
            }
        else:
            signal = {
                "action": "sell",
                "price": current_price,
                "stop_loss": current_price + stop_loss_distance,
                "take_profit": current_price - take_profit_distance,
                "position_size": position_size,
                "timeframe": timeframe,  # Include timeframe in the signal
            }

        return signal