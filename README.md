# XAUUSD AI Trader

An intelligent automated trading bot for XAUUSD (Gold/USD) with AI-powered signals, real-time monitoring, and risk management.

## 🏆 Features

- ✅ **AI-Powered Signals**: XGBoost model trained on technical indicators
- 📊 **Real-time Market Analysis**: EMA, RSI, MACD indicators
- 💰 **Risk Management**: Automated position sizing and stop-loss/take-profit
- 📱 **Mobile Dashboard**: Flutter app for monitoring trades
- 🤖 **Automated Alerts**: Telegram notifications for signals and closed trades
- 🔌 **MetaTrader 5 Integration**: Direct MT5 API connectivity
- 📈 **Backtesting Support**: Test strategies on historical data
- 🐳 **Docker Ready**: Easy deployment with Docker

## ⚠️ Important Disclaimer

**This is an educational trading system.** Trading carries risk. Start with:
1. Paper trading (demo account) for 2-4 weeks
2. Risk only what you can afford to lose
3. Monitor performance continuously
4. Use proper risk management (2% risk per trade max)

No guarantees of profit are made.

## 🏗️ Project Structure

```
xauusd-ai-trader/
├── backend/              # FastAPI trading engine
│   ├── app.py           # Main application
│   ├── mt5_connector.py  # MT5 integration
│   ├── strategy.py       # Technical indicators
│   ├── risk_manager.py   # Risk management
│   ├── telegram_bot.py   # Telegram alerts
│   └── requirements.txt  # Dependencies
├── ai/                  # Machine learning
│   ├── train_model.py   # Model training
│   ├── predict.py       # Predictions
│   └── models/          # Trained models
├── mobile_app/          # Flutter application
│   └── flutter_app/
├── docs/                # Documentation
├── docker-compose.yml   # Docker configuration
└── README.md
```

## 🚀 Quick Start

### 1. Setup

```bash
# Clone repository
git clone https://github.com/Roaring-panda/xauusd-ai-trader.git
cd xauusd-ai-trader

# Configure environment
cp .env.example .env
# Edit .env with your MT5 credentials and Telegram token
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run Backend

**With Docker:**
```bash
docker-compose up
```

**Without Docker:**
```bash
cd backend
uvicorn app:app --reload
```

### 4. Configure Mobile App

```bash
cd mobile_app/flutter_app
flutter pub get
flutter run
```

## 📖 Documentation

- [Setup Guide](docs/setup.md) - Installation and configuration
- [Architecture](docs/architecture.md) - System design and components

## 🎓 Development Phases

1. ✅ MT5 connection and account info
2. ✅ Market data collection (OHLC)
3. ✅ Technical indicator strategy
4. ✅ Risk management system
5. ✅ Telegram alerts
6. ⚙️ AI model training (XGBoost)
7. ⚙️ Flutter mobile dashboard
8. ⚙️ VPS deployment setup
9. ⚙️ Backtesting framework
10. ⚙️ Live trading (after testing)

## 📊 Trading Strategy

### Technical Indicators

- **EMA 50 & EMA 200**: Trend identification
- **RSI 14**: Momentum and overbought/oversold levels
- **MACD**: Momentum and trend changes

### Signal Logic

```python
BUY:  EMA50 > EMA200 AND RSI > 55 AND MACD > Signal
SELL: EMA50 < EMA200 AND RSI < 45 AND MACD < Signal
HOLD: Otherwise
```

### AI Enhancement

XGBoost classifier trained on:
- OHLC data
- Technical indicators
- Historical patterns

## 💾 Configuration

Key settings in `.env`:

```env
MT5_LOGIN=your_login
MT5_PASSWORD=your_password
MT5_SERVER=your_server
TELEGRAM_TOKEN=your_bot_token
RISK_PERCENT=2.0  # Risk per trade
```

## 📈 Risk Management

- **Position Sizing**: Based on 2% risk per trade (configurable)
- **Stop-Loss**: Technical level below entry
- **Take-Profit**: Risk-reward ratio 2:1
- **Margin Check**: Prevents over-leveraging

## 🔐 Security

- Credentials stored in `.env` (not in repo)
- API keys not hardcoded
- Telegram bot token protected
- MT5 account isolation

## 📞 Support

For issues:
1. Check [Setup Guide](docs/setup.md)
2. Review [Architecture](docs/architecture.md)
3. Check MT5 connection logs
4. Verify environment variables

## 📝 License

See [LICENSE](LICENSE) file.

## 🤝 Contributing

Contributions welcome! Please:
1. Test thoroughly
2. Start with demo trading
3. Document changes
4. Follow best practices

---

**Remember**: This is a learning project. Always test with demo accounts first!
