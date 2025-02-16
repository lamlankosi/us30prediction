# strategy.py
import pandas as pd
import numpy as np

class TradingStrategy:
    def __init__(self, short_window=10, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def analyze(self, data):
        """Analyze market data and generate trading signals."""
        data['short_ma'] = data['close'].rolling(window=self.short_window).mean()
        data['long_ma'] = data['close'].rolling(window=self.long_window).mean()
        data['signal'] = np.where(data['short_ma'] > data['long_ma'], 1, -1)
        return data

    def generate_signal(self, data):
        """Generate a buy/sell signal based on the latest data."""
        latest_signal = data['signal'].iloc[-1]
        return "buy" if latest_signal == 1 else "sell"