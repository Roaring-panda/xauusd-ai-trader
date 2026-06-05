import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)

def connect(login, password, server):
    """
    Connect to MetaTrader 5
    
    Args:
        login: MT5 login
        password: MT5 password
        server: MT5 server name
    
    Returns:
        bool: True if connected, False otherwise
    """
    try:
        if not mt5.initialize(
            login=int(login),
            password=password,
            server=server
        ):
            logger.error("Failed to initialize MT5")
            return False
        logger.info("Connected to MT5")
        return True
    except Exception as e:
        logger.error(f"MT5 connection error: {e}")
        return False

def get_account_info():
    """
    Get account information from MT5
    
    Returns:
        dict: Account information
    """
    try:
        account_info = mt5.account_info()
        if account_info:
            return {
                "balance": account_info.balance,
                "equity": account_info.equity,
                "margin": account_info.margin,
                "free_margin": account_info.free_margin
            }
    except Exception as e:
        logger.error(f"Error getting account info: {e}")
    return None

def disconnect():
    """
    Disconnect from MetaTrader 5
    """
    mt5.shutdown()
    logger.info("Disconnected from MT5")
