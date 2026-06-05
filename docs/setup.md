# Setup Guide

## Prerequisites

- Python 3.8+
- MetaTrader 5
- Docker & Docker Compose
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Roaring-panda/xauusd-ai-trader.git
cd xauusd-ai-trader
```

### 2. Setup Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run with Docker

```bash
docker-compose up -d
```

### 5. Start Backend (without Docker)

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 5000
```

## Trading Strategy

**IMPORTANT**: Start with paper trading before using live accounts.

The bot uses:
- EMA 50 and EMA 200 for trend
- RSI 14 for momentum
- MACD for confirmation

## Risk Management

- Risk per trade: 2% of balance (configurable)
- Stop-loss: Based on strategy levels
- Take-profit: Risk-reward ratio 2:1

## Testing

### 1. Demo Trading

Connect to MT5 demo account to test without real money.

### 2. Backtesting

```bash
python ai/train_model.py
```

## Troubleshooting

### MT5 Connection Issues

- Verify login credentials
- Check server name
- Ensure MT5 is running

### Telegram Issues

- Verify bot token and chat ID
- Check internet connection

## Next Steps

1. Configure MT5 credentials
2. Test connection with demo account
3. Train AI model on historical data
4. Run paper trading for 2-4 weeks
5. Monitor performance metrics
6. Deploy to VPS once confident
