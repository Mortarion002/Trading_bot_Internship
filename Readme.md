# Binance Futures Testnet Trading Bot

A CLI trading bot that places Market and Limit orders on Binance Futures Testnet (USDT-M), with structured logging, Pydantic validation, and Rich terminal output.

## Project Structure
```
trading_bot/
  bot/
    __init__.py
    client.py          # Binance testnet client wrapper
    orders.py          # Order placement logic
    validators.py      # Pydantic input validation
    logging_config.py  # Logging setup (file + console)
  venv/
  cli.py               # CLI entry point (Typer)
  .env                 # API credentials (not committed)
  .env.example         # Credential template
  market_order.log     # Market order log output
  limit_order.log      # Limit order log output
  requirements.txt
  README.md
```

## Setup

### 1. Get Testnet API Credentials
- Go to **https://testnet.binancefuture.com** (log in with GitHub)
- Click **"API Key"** at the top and generate a key
- These are separate from your real Binance credentials

### 2. Clone and install dependencies
```bash
git clone <your-repo-url>
cd trading_bot

python3 -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```

Open `.env` and fill in your testnet credentials:
```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

## How to Run

### Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002 --log-file market_order.log
```

### Limit Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 83000 --log-file limit_order.log
```

### All Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--symbol` | `-s` | Yes | Trading pair, e.g. `BTCUSDT` |
| `--side` | | Yes | `BUY` or `SELL` |
| `--type` | `-t` | Yes | `MARKET` or `LIMIT` |
| `--quantity` | `-q` | Yes | Amount to trade |
| `--price` | `-p` | LIMIT only | Limit price |

### Help
```bash
python cli.py --help
```

## Validation Rules

- Symbol must end in `USDT` (e.g. `BTCUSDT`, `ETHUSDT`)
- Quantity must be greater than 0
- Minimum order notional value is **$100** (Binance requirement)
- Price is required for LIMIT orders and must be omitted for MARKET orders

## Logging

All API requests, responses, and errors are logged with timestamps.

- `market_order.log` — market order activity
- `limit_order.log` — limit order activity

Log format:
```
2026-03-13 20:48:20 | INFO | trading_bot | Order placed successfully — response: {...}
```

## Assumptions

- Only USDT-M perpetual futures are supported (symbols must end in `USDT`)
- Limit orders use `GTC` (Good Till Cancelled) time-in-force by default
- Testnet environment may have limited liquidity; orders may not fill immediately
- Real Binance API keys will **not** work — testnet credentials are required