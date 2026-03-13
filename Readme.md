# Binance Futures Testnet Trading Bot

A CLI trading bot that places Market and Limit orders on Binance Futures Testnet (USDT-M).

## Setup

### 1. Register on Binance Futures Testnet
Go to https://testnet.binancefuture.com and generate API credentials.

### 2. Clone and set up the project
```bash
git clone <your-repo-url>
cd trading_bot

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Open .env and fill in your API key and secret
```

## How to Run

### Market Order (BUY)
```bash
python cli.py place-order BTCUSDT BUY MARKET 0.001
```

### Limit Order (SELL)
```bash
python cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 95000.50
```

### Help
```bash
python cli.py --help
python cli.py place-order --help
```

## Logs
All API requests, responses, and errors are written to `trading_bot.log` in the project root.

## Assumptions
- Only USDT-M perpetual futures are supported (symbols must end in USDT)
- Limit orders use GTC (Good Till Cancelled) time-in-force by default
- The testnet environment may have limited liquidity; orders may not fill immediately