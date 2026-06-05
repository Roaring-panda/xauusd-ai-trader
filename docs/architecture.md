# Architecture

## System Overview

The XAUUSD AI Trader is a distributed system with three main components:

```
┌──────────────────────────┐
│   Mobile App             │
│    (Flutter)             │
└──────────────┬───────────┘
               │
               │ REST API
               │
        ┌──────┴──────────────┐
        │   Backend           │
        │   (FastAPI)         │
        └──────┬──────────────┘
             │
    ┌────────┴────────────────┬──────────────────┬──────────────────┐
    │                         │                  │                  │
    │                         │                  │                  │
┌──┴───────────┐    ┌────────┴─────┐     ┌──────┴──────┐
│   MT5        │    │   AI         │     │  Telegram   │
│              │    │  Model       │     │    Bot      │
└──────────────┘    └──────────────┘     └─────────────┘
```

## Components

### 1. Backend (FastAPI)

**Purpose**: Central trading engine and API server

**Modules**:

- `app.py`: FastAPI application with REST endpoints
- `mt5_connector.py`: MT5 connection and account management
- `market_data.py`: Fetch real-time price data
- `strategy.py`: Technical indicator calculations
- `risk_manager.py`: Position sizing and risk calculations
- `telegram_bot.py`: Alert notifications

**API Endpoints**:

```
GET  /               - Health check
GET  /health         - Detailed health
GET  /account        - Account info
GET  /current-price  - Current price
POST /trade          - Open trade
GET  /positions      - Open positions
GET  /history        - Trade history
```

### 2. AI Module

**Purpose**: ML-based signal generation

**Features**:

- `train_model.py`: Train XGBoost classifier
- `predict.py`: Make predictions

**Input Features**:
- OHLC (Open, High, Low, Close)
- Volume
- RSI, MACD, EMA50, EMA200

**Output**:
```
1  = BUY
0  = HOLD
-1 = SELL
```

### 3. Mobile App (Flutter)

**Purpose**: Real-time monitoring and alerts

**Screens**:
- Dashboard: Account balance, current signal
- Positions: Open trades
- History: Trade history and P&L
- Alerts: Push notifications
- Settings: Configuration

## Data Flow

### Trading Cycle

1. **Market Data Collection** (Every 15 minutes)
   ```
   MT5 → MarketData → OHLC DataFrame
   ```

2. **Indicator Calculation**
   ```
   OHLC → Strategy → EMA, RSI, MACD
   ```

3. **Signal Generation**
   ```
   Indicators → AI Model → Prediction (BUY/HOLD/SELL)
   ```

4. **Risk Assessment**
   ```
   Signal → RiskManager → Position Size, SL/TP
   ```

5. **Trade Execution**
   ```
   RiskManager → MT5Connector → Open Position
   ```

6. **Notification**
   ```
   Trade Event → TelegramBot → Alert to User
   Mobile App → REST API → Update Dashboard
   ```

## Database Schema

### Trades Table

```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10),
    direction VARCHAR(4),  -- BUY/SELL
    entry_price FLOAT,
    entry_time TIMESTAMP,
    exit_price FLOAT,
    exit_time TIMESTAMP,
    quantity FLOAT,
    profit_loss FLOAT,
    status VARCHAR(10)     -- OPEN/CLOSED
);
```

### Signals Table

```sql
CREATE TABLE signals (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP,
    symbol VARCHAR(10),
    signal INTEGER,        -- 1=BUY, 0=HOLD, -1=SELL
    confidence FLOAT,
    rsi FLOAT,
    macd FLOAT,
    ema50 FLOAT,
    ema200 FLOAT
);
```

## Deployment Architecture

### Development

```
Local Machine
├── Backend (FastAPI)
├── AI Training
└── Mobile App (emulator)
```

### Production

```
VPS (Ubuntu)
├── Docker Container (Backend)
├── MT5 Terminal
└── Telegram Bot

Mobile Device
└── Flutter APK

CI/CD
└── GitHub Actions
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` file
2. **API Keys**: Use Telegram bot token, MT5 credentials securely
3. **HTTPS**: Use TLS for API endpoints in production
4. **Account Protection**: Limit API exposure, use IP whitelisting

## Performance Metrics

### Target KPIs

- **Win Rate**: >55%
- **Profit Factor**: >1.5 (Profit/Loss)
- **Max Drawdown**: <20% of equity
- **Sharpe Ratio**: >1.0

### Monitoring

Track in Telegram alerts and mobile dashboard:
- Daily P&L
- Win/Loss ratio
- Current equity
- Open positions

## Scaling

### Horizontal Scaling

- Load balancer for backend
- Database replication
- Message queue for async tasks

### Vertical Scaling

- Increase VPS resources
- Optimize database queries
- Implement caching (Redis)
