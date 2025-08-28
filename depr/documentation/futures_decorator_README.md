# FuturesAPIDecorator

A decorator utility for cryptocurrency futures trading APIs that adds logging and notification capabilities to trading operations.

## Features

- Automatically log all trading actions (market orders, limit orders, position closures, etc.)
- Send real-time notifications via Telegram for trading operations
- Record both successful and failed trading actions
- Preserve the original API functionality while adding monitoring capabilities
- Dynamic decoration of API methods based on their type
- Compatible with any futures trading API that follows the AbstractFuturesAPI interface

## Installation

### Dependencies

This utility requires the following packages:
- `python-telegram-bot` (for notifications)
- `pytz` (for timezone-aware logging)

Additionally, it depends on the following local modules:
- `logger` (for writing logs)
- `tgbot` (for sending Telegram notifications)

```bash
# Install required packages
pip install python-telegram-bot pytz

# Or install from requirements.txt (recommended)
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from futures_decorator import FuturesAPIDecorator
from your_exchange_module import YourExchangeAPI

# Initialize your trading API
exchange_api = YourExchangeAPI(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

# Wrap it with the decorator
decorated_api = FuturesAPIDecorator(
    api=exchange_api,
    token="YOUR_TELEGRAM_BOT_TOKEN",
    chat_id="YOUR_TELEGRAM_CHAT_ID"
)

# Use the decorated API normally - logging and notifications are automatic
decorated_api.place_market_order(
    symbol="BTC/USDT", 
    position_type="LONG", 
    leverage=5,
    amount=100.0,
    stop_loss_price=19500.0,
    take_profit_price=21000.0
)
```

### Using with Binance Futures API

```python
from futures_decorator import FuturesAPIDecorator
from CryptoAPI.futures.binance_api import BinanceFutures

# Initialize Binance Futures API
binance_api = BinanceFutures()

# Create decorated API
decorated_api = FuturesAPIDecorator(
    api=binance_api,
    token="YOUR_TELEGRAM_BOT_TOKEN",
    chat_id="YOUR_TELEGRAM_CHAT_ID"
)

# Execute trades with automatic logging and notifications
decorated_api.place_market_order("ETH/USDT", "LONG", 10, 200.0)
decorated_api.close_position("BTC/USDT", "SHORT")

# Informational methods work as before without additional logging
balance = decorated_api.fetch_usdt_balance()
price = decorated_api.get_price("BTC/USDT")
```

### Custom Logger and TelegramBot Integration

```python
from futures_decorator import FuturesAPIDecorator
from CryptoAPI.futures.binance_api import BinanceFutures
from logger import Logger
from tgbot import TelegramBot

# Create custom logger and telegram bot
custom_logger = Logger(log_dir="/custom/log/path")
custom_tgbot = TelegramBot(token="YOUR_TOKEN", chat_id="YOUR_CHAT_ID")

# Initialize API with custom components
binance_api = BinanceFutures()
decorated_api = FuturesAPIDecorator(
    api=binance_api,
    logger=custom_logger,
    tgbot=custom_tgbot
)

# Use decorated API
decorated_api.place_limit_order("BTC/USDT", "LONG", 20000.0, 5, 100.0)
```

## Trading Methods with Logging

The following trading methods automatically trigger logging and notifications:

1. `set_stop_loss_take_profit` - Setting stop loss and take profit levels
2. `place_market_order` - Executing market orders
3. `place_limit_order` - Placing limit orders
4. `close_position` - Closing open positions
5. `cancel_order` - Cancelling pending orders

## Information Methods (Pass-through)

These methods are passed through directly without additional logging/notifications:

1. `get_positions` - Getting current positions
2. `get_open_orders` - Retrieving open orders
3. `fetch_usdt_balance` - Getting account balance
4. `get_price` - Getting current price
5. `get_historical_data` - Retrieving historical data

## API Reference

### Constructor

- `FuturesAPIDecorator(api, logger=None, tgbot=None, log_dir=None, token=None, chat_id=None)` - Initialize with your API and notification settings
  - `api`: An instance of a class implementing the AbstractFuturesAPI interface (required)
  - `logger`: Optional custom Logger instance
  - `tgbot`: Optional custom TelegramBot instance
  - `log_dir`: Directory for logs (if creating a new Logger)
  - `token`: Telegram bot token (if creating a new TelegramBot)
  - `chat_id`: Telegram chat ID (if creating a new TelegramBot)

### Decorated Methods

All methods from your original API are available with the same signatures. Trading methods will have additional logging and notification functionality.
