import requests
import logging

logger = logging.getLogger(__name__)

class TelegramBot:
    """
    Telegram bot for sending trading alerts
    """
    
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
    
    def send_message(self, text):
        """
        Send a message to Telegram
        
        Args:
            text: Message text
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            url = f"{self.base_url}/sendMessage"
            response = requests.post(
                url,
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "HTML"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Message sent successfully")
                return True
            else:
                logger.error(f"Failed to send message: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Telegram error: {e}")
            return False
    
    def send_buy_signal(self, symbol, price, signal_strength):
        """
        Send buy signal alert
        """
        message = f"""🟢 <b>BUY SIGNAL</b>
        
Symbol: {symbol}
Price: {price:.2f}
Signal Strength: {signal_strength:.2f}"""
        return self.send_message(message)
    
    def send_sell_signal(self, symbol, price, signal_strength):
        """
        Send sell signal alert
        """
        message = f"""🔴 <b>SELL SIGNAL</b>
        
Symbol: {symbol}
Price: {price:.2f}
Signal Strength: {signal_strength:.2f}"""
        return self.send_message(message)
    
    def send_trade_closed(self, symbol, profit_loss, entry_price, exit_price):
        """
        Send trade closed alert
        """
        pnl_emoji = "📈" if profit_loss > 0 else "📉"
        message = f"""{pnl_emoji} <b>TRADE CLOSED</b>
        
Symbol: {symbol}
Entry: {entry_price:.2f}
Exit: {exit_price:.2f}
P&L: ${profit_loss:.2f}"""
        return self.send_message(message)
