import logging

logger = logging.getLogger(__name__)

class RiskManager:
    """
    Risk management module for position sizing and stop-loss/take-profit calculation
    """
    
    @staticmethod
    def calculate_position_size(balance, risk_percent, entry_price, stop_loss_price):
        """
        Calculate position size based on risk management rules
        
        Args:
            balance: Account balance
            risk_percent: Risk percentage per trade (e.g., 2.0 for 2%)
            entry_price: Entry price
            stop_loss_price: Stop-loss price
        
        Returns:
            float: Position size in lots
        """
        if entry_price == stop_loss_price:
            logger.error("Entry price cannot equal stop-loss price")
            return 0
        
        risk_amount = balance * (risk_percent / 100)
        price_difference = abs(entry_price - stop_loss_price)
        
        # Calculate position size (simplified, actual calculation depends on contract specs)
        position_size = risk_amount / (price_difference * 100)
        
        logger.info(f"Position size: {position_size:.2f} lots")
        return position_size
    
    @staticmethod
    def calculate_take_profit(entry_price, stop_loss_price, risk_reward_ratio=2.0):
        """
        Calculate take-profit level based on risk-reward ratio
        
        Args:
            entry_price: Entry price
            stop_loss_price: Stop-loss price
            risk_reward_ratio: Risk-reward ratio (default 2:1)
        
        Returns:
            float: Take-profit price
        """
        risk = abs(entry_price - stop_loss_price)
        take_profit = entry_price + (risk * risk_reward_ratio)
        return take_profit
    
    @staticmethod
    def validate_position(balance, position_size, margin_required):
        """
        Validate if position can be opened based on available margin
        
        Args:
            balance: Account balance
            position_size: Position size in lots
            margin_required: Margin required per lot
        
        Returns:
            bool: True if position is valid, False otherwise
        """
        total_margin = position_size * margin_required
        available_margin = balance * 0.5  # Keep 50% buffer
        
        if total_margin > available_margin:
            logger.warning(f"Insufficient margin: {total_margin} > {available_margin}")
            return False
        
        return True
