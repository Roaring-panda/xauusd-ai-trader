# XAUUSD AI Trader - React Native Expo App

React Native mobile app for XAUUSD AI Trader, compatible with Expo Go.

## Quick Start

### 1. Install Dependencies
```bash
cd mobile_app/expo_app
npm install
```

### 2. Get Your Backend IP
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```
Find your local IP (192.168.x.x or 10.x.x.x)

### 3. Start Backend
```bash
cd backend
python app.py
```

### 4. Start Expo
```bash
cd mobile_app/expo_app
npm start
```

### 5. Open on Your Phone
1. Download Expo Go from App Store or Google Play
2. Scan the QR code in terminal
3. App loads on your phone

### 6. Configure API
1. Go to Settings tab
2. Enter: `http://192.168.x.x:5000` (replace with your IP)
3. Tap Save
4. Tap Test Connection

## Features

📊 **Dashboard**
- Real-time price
- Current signal
- Account status
- Technical indicators

📈 **Signals**
- Trading signals (BUY/SELL/HOLD)
- EMA, RSI, MACD indicators
- Trend analysis

💰 **Account**
- Balance and equity
- P&L tracking
- Margin info
- Risk analysis

⚙️ **Settings**
- API configuration
- Connection testing
- Telegram notifications

## Troubleshooting

**Cannot reach API?**
- Verify backend is running
- Check IP address is correct
- Ensure same WiFi network
- Disable VPN

**Connection refused?**
- Backend must be on port 5000
- Check firewall settings
- Try: `curl http://192.168.x.x:5000/health`

## Development

```bash
# Hot reload - changes auto-reload
# Press 'j' for debugger
# Press 'r' for restart
```

## Building

```bash
# Android APK
expo build:android

# iOS App
expo build:ios
```

## Security
⚠️ Development only - Use HTTPS and proper auth in production

## License
MIT
