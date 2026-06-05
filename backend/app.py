from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Dict, List, Optional

from config import (
    MT5_LOGIN, MT5_PASSWORD, MT5_SERVER,
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID,
    SYMBOL, TIMEFRAME, RISK_PERCENT
)
from mt5_connector import connect, disconnect, get_account_info
from market_data import MarketData
from strategy import TradingStrategy
from risk_manager import RiskManager
from telegram_bot import TelegramBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global state
mt5_connected = False
bot = None
market_data = MarketData()
strategy = TradingStrategy()
risk_manager = RiskManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI app
    Handles startup and shutdown
    """
    # Startup
    global mt5_connected, bot
    logger.info("Starting up...")
    
    try:
        if connect(MT5_LOGIN, MT5_PASSWORD, MT5_SERVER):
            mt5_connected = True
            logger.info("MT5 connection established")
        else:
            logger.warning("Failed to connect to MT5")
    except Exception as e:
        logger.error(f"Startup error: {e}")
    
    # Initialize Telegram bot
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        bot = TelegramBot(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
        logger.info("Telegram bot initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    try:
        disconnect()
        mt5_connected = False
        logger.info("MT5 connection closed")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

app = FastAPI(
    title="XAUUSD AI Trader",
    description="AI-powered automated trading bot for XAUUSD (Gold/USD)",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
async def root() -> Dict:
    """
    API root endpoint with documentation
    """
    return {
        "service": "XAUUSD AI Trader",
        "version": "1.0.0",
        "status": "running",
        "description": "AI-powered automated trading bot for XAUUSD",
        "endpoints": {
            "GET /health": "Health check",
            "GET /status": "Detailed status",
            "GET /account": "Account information",
            "GET /market/price": "Current market price",
            "GET /market/candles": "Get OHLC candles",
            "GET /strategy/signal": "Generate trading signal",
            "POST /trade/calculate": "Calculate trade parameters",
            "GET /telegram/test": "Test Telegram notification"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check() -> Dict:
    """
    Simple health check endpoint
    """
    return {
        "status": "healthy",
        "service": "XAUUSD AI Trader",
        "mt5_connected": mt5_connected
    }

@app.get("/status", tags=["Health"])
async def status() -> Dict:
    """
    Detailed status information
    """
    return {
        "service": "XAUUSD AI Trader",
        "version": "1.0.0",
        "status": "running",
        "mt5_connected": mt5_connected,
        "symbol": SYMBOL,
        "timeframe": TIMEFRAME,
        "risk_percent": RISK_PERCENT,
        "telegram_bot": bot is not None
    }

# ============================================================================
# ACCOUNT ENDPOINTS
# ============================================================================

@app.get("/account", tags=["Account"])
async def get_account() -> Dict:
    """
    Get account information from MT5
    """
    if not mt5_connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    
    try:
        account_info = get_account_info()
        if account_info:
            return {
                "success": True,
                "account": account_info
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to get account info")
    except Exception as e:
        logger.error(f"Account error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# MARKET DATA ENDPOINTS
# ============================================================================

@app.get("/market/price", tags=["Market Data"])
async def get_current_price() -> Dict:
    """
    Get current market price for XAUUSD
    """
    if not mt5_connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    
    try:
        price = market_data.get_current_price(SYMBOL)
        if price:
            return {
                "success": True,
                "symbol": SYMBOL,
                "price": price
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to get price")
    except Exception as e:
        logger.error(f"Price error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/bid-ask", tags=["Market Data"])
async def get_bid_ask() -> Dict:
    """
    Get current bid and ask prices
    """
    if not mt5_connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    
    try:
        bid, ask = market_data.get_bid_ask(SYMBOL)
        if bid and ask:
            return {
                "success": True,
                "symbol": SYMBOL,
                "bid": bid,
                "ask": ask,
                "spread": ask - bid
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to get bid/ask")
    except Exception as e:
        logger.error(f"Bid/Ask error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/candles", tags=["Market Data"])
async def get_candles(count: int = Query(100, ge=10, le=1000)) -> Dict:
    """
    Get OHLC candlestick data
    
    Query Parameters:
        - count: Number of candles (10-1000, default: 100)
    """
    if not mt5_connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    
    try:
        import MetaTrader5 as mt5
        timeframe = mt5.TIMEFRAME_M15  # 15-minute candles
        
        df = market_data.get_candles(SYMBOL, timeframe, count)
        if df is not None:
            return {
                "success": True,
                "symbol": SYMBOL,
                "timeframe": "M15",
                "count": len(df),
                "data": df.to_dict('records')
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to get candles")
    except Exception as e:
        logger.error(f"Candles error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# STRATEGY & SIGNAL ENDPOINTS
# ============================================================================

@app.get("/strategy/signal", tags=["Strategy"])
async def generate_signal() -> Dict:
    """
    Generate trading signal based on current market conditions
    """
    if not mt5_connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    
    try:
        import MetaTrader5 as mt5
        timeframe = mt5.TIMEFRAME_M15
        
        # Get candles
        df = market_data.get_candles(SYMBOL, timeframe, 200)
        if df is None:
            raise HTTPException(status_code=500, detail="Failed to get market data")
        
        # Calculate indicators
        close_prices = df['close']
        
        ema50 = strategy.calculate_ema(close_prices, 50)
        ema200 = strategy.calculate_ema(close_prices, 200)
        rsi = strategy.calculate_rsi(close_prices, 14)
        macd, signal_line, histogram = strategy.calculate_macd(close_prices)
        
        # Get latest values
        ema50_val = ema50.iloc[-1]
        ema200_val = ema200.iloc[-1]
        rsi_val = rsi.iloc[-1]
        macd_val = macd.iloc[-1]
        signal_val = signal_line.iloc[-1]
        
        # Generate signal
        signal = strategy.generate_signal(ema50_val, ema200_val, rsi_val, macd_val, signal_val)
        
        signal_names = {1: "BUY", 0: "HOLD", -1: "SELL"}
        
        return {
            "success": True,
            "signal": signal_names[signal],
            "signal_code": signal,
            "indicators": {
                "ema50": float(ema50_val),
                "ema200": float(ema200_val),
                "rsi14": float(rsi_val),
                "macd": float(macd_val),
                "signal_line": float(signal_val),
                "histogram": float(histogram.iloc[-1])
            }
        }
    except Exception as e:
        logger.error(f"Signal generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/strategy/indicators", tags=["Strategy"])
async def get_indicators() -> Dict:
    """
    Get current technical indicators
    """
    if not mt5_connected:
        raise HTTPException(status_code=503, detail="MT5 not connected")
    
    try:
        import MetaTrader5 as mt5
        timeframe = mt5.TIMEFRAME_M15
        
        df = market_data.get_candles(SYMBOL, timeframe, 200)
        if df is None:
            raise HTTPException(status_code=500, detail="Failed to get market data")
        
        close_prices = df['close']
        
        ema50 = strategy.calculate_ema(close_prices, 50).iloc[-1]
        ema200 = strategy.calculate_ema(close_prices, 200).iloc[-1]
        rsi = strategy.calculate_rsi(close_prices, 14).iloc[-1]
        macd, signal, histogram = strategy.calculate_macd(close_prices)
        
        return {
            "success": True,
            "indicators": {
                "ema50": float(ema50),
                "ema200": float(ema200),
                "rsi14": float(rsi),
                "macd": float(macd.iloc[-1]),
                "signal_line": float(signal.iloc[-1]),
                "histogram": float(histogram.iloc[-1])
            }
        }
    except Exception as e:
        logger.error(f"Indicators error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# RISK MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/trade/calculate", tags=["Risk Management"])
async def calculate_trade_parameters(
    entry_price: float = Query(..., gt=0),
    stop_loss: float = Query(..., gt=0),
    balance: float = Query(..., gt=0),
    risk_reward_ratio: float = Query(2.0, gt=0)
) -> Dict:
    """
    Calculate trade parameters (position size, take-profit, etc.)
    
    Query Parameters:
        - entry_price: Entry price
        - stop_loss: Stop-loss price
        - balance: Account balance
        - risk_reward_ratio: Risk-reward ratio (default: 2.0)
    """
    try:
        position_size = risk_manager.calculate_position_size(
            balance, RISK_PERCENT, entry_price, stop_loss
        )
        take_profit = risk_manager.calculate_take_profit(
            entry_price, stop_loss, risk_reward_ratio
        )
        
        return {
            "success": True,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "position_size": position_size,
            "risk_amount": balance * (RISK_PERCENT / 100),
            "risk_reward_ratio": risk_reward_ratio
        }
    except Exception as e:
        logger.error(f"Trade calculation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trade/position-size", tags=["Risk Management"])
async def get_position_size(
    balance: float = Query(..., gt=0),
    entry_price: float = Query(..., gt=0),
    stop_loss: float = Query(..., gt=0)
) -> Dict:
    """
    Get recommended position size
    """
    try:
        position_size = risk_manager.calculate_position_size(
            balance, RISK_PERCENT, entry_price, stop_loss
        )
        
        return {
            "success": True,
            "position_size": position_size,
            "risk_percent": RISK_PERCENT,
            "risk_amount": balance * (RISK_PERCENT / 100)
        }
    except Exception as e:
        logger.error(f"Position size error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TELEGRAM ENDPOINTS
# ============================================================================

@app.get("/telegram/test", tags=["Notifications"])
async def test_telegram() -> Dict:
    """
    Test Telegram notification
    """
    if not bot:
        raise HTTPException(status_code=503, detail="Telegram bot not configured")
    
    try:
        success = bot.send_message("🤖 Telegram bot is working! This is a test message.")
        return {
            "success": success,
            "message": "Test message sent" if success else "Failed to send message"
        }
    except Exception as e:
        logger.error(f"Telegram test error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/telegram/send", tags=["Notifications"])
async def send_telegram_message(message: str = Query(...)) -> Dict:
    """
    Send a custom message via Telegram
    
    Query Parameters:
        - message: Message text to send
    """
    if not bot:
        raise HTTPException(status_code=503, detail="Telegram bot not configured")
    
    try:
        success = bot.send_message(message)
        return {
            "success": success,
            "message": "Message sent" if success else "Failed to send message"
        }
    except Exception as e:
        logger.error(f"Send message error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "message": "Use GET / for API documentation"
        }
    )

@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
