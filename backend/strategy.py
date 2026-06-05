import logging
import numpy as np

logger = logging.getLogger(__name__)

class TradingStrategy:
    """
    Trading strategy using technical indicators
    """
    
    @staticmethod
    def calculate_ema(prices, period):
        """
        Calculate Exponential Moving Average
        """
        return prices.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(prices, period=14):
        """
        Calculate Relative Strength Index
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(prices, fast=12, slow=26, signal=9):
        """
        Calculate MACD (Moving Average Convergence Divergence)
        """
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram
    
    @staticmethod
    def generate_signal(ema50, ema200, rsi, macd, signal_line):
        """
        Generate trading signal based on indicators
        
        Returns:
            1: BUY
            0: HOLD
            -1: SELL
        """
        if ema50 > ema200 and rsi > 55 and macd > signal_line:
            return 1  # BUY
        elif ema50 < ema200 and rsi < 45 and macd < signal_line:
            return -1  # SELL
        else:
            return 0  # HOLD
