import MetaTrader5 as mt5
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class MarketData:
    """
    Handle market data retrieval from MetaTrader 5
    """
    
    @staticmethod
    def get_candles(symbol, timeframe, count=100):
        """
        Fetch candlestick data from MT5
        
        Args:
            symbol: Trading symbol (e.g., "XAUUSD")
            timeframe: Timeframe constant from mt5
            count: Number of candles to fetch
        
        Returns:
            pd.DataFrame: OHLC data
        """
        try:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            if rates is None:
                logger.error(f"Failed to get rates for {symbol}")
                return None
            
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        except Exception as e:
            logger.error(f"Error fetching candles: {e}")
            return None
    
    @staticmethod
    def get_current_price(symbol):
        """
        Get current price for a symbol
        
        Args:
            symbol: Trading symbol
        
        Returns:
            float: Current bid price
        """
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                return tick.bid
            return None
        except Exception as e:
            logger.error(f"Error getting current price: {e}")
            return None
    
    @staticmethod
    def get_bid_ask(symbol):
        """
        Get current bid and ask prices
        
        Args:
            symbol: Trading symbol
        
        Returns:
            tuple: (bid, ask) prices
        """
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                return tick.bid, tick.ask
            return None, None
        except Exception as e:
            logger.error(f"Error getting bid/ask: {e}")
            return None, None
