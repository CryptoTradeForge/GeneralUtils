# General Utilities

A collection of utility modules for common development tasks in Python applications.

## Available Utilities

### ConfigReader
A flexible configuration management utility that allows you to:
- Read configuration values from environment variables (.env files)
- Parse YAML configuration files
- Retrieve individual settings or entire configuration sections
- Access nested configuration with a clean, consistent API

[View detailed ConfigReader documentation](./documentation/config_reader_README.md)

### Logger
A robust logging utility with advanced features:
- Write timestamped log messages to rotating daily files
- Separate general logs from error logs
- Full timezone support for accurate timestamps across different regions
- Handle various time formats (timestamps, datetime objects, string dates)
- Configurable log retention policies

[View detailed Logger documentation](./documentation/logger_README.md)

### TelegramBot
A simple utility for sending Telegram notifications:
- Send text messages to specified Telegram chat IDs
- Easy integration with other applications
- Simple API with minimal dependencies
- Error handling for API communication issues

[View detailed TelegramBot documentation](./documentation/tgbot_README.md)

### FuturesAPIDecorator
A decorator utility for cryptocurrency futures trading APIs:
- Automatically log all trading actions (market orders, limit orders, position closures)
- Send real-time notifications via Telegram for trading operations
- Record both successful and failed trading actions
- Compatible with any futures trading API that follows the AbstractFuturesAPI interface

[View detailed FuturesAPIDecorator documentation](./documentation/futures_decorator_README.md)

## Installation

### Using pip

```bash
# Install directly
pip install python-dotenv pytz python-telegram-bot

# Or install from requirements.txt
pip install -r requirements.txt
```

A `requirements.txt` file is included in the repository for easy installation of dependencies.

## Quick Start

### ConfigReader Example

```python
from config_reader import ConfigReader

# Initialize with default paths (.env and config.yaml)
config = ConfigReader()

# Read from environment variables
api_key = config.get_env("API_KEY")
debug_mode = config.get_env("DEBUG_MODE", "False")

# Read values from config.yaml
max_retries = config.get_config("network", "max_retries")
timeout = config.get_config("network", "timeout")
# Access deeply nested values
db_host = config.get_config("database", "connection", "host")
```

### Logger Example

```python
from logger import Logger

# Initialize with default settings
logger = Logger()

# Write general logs
logger.write_log("Application started")
logger.write_log("Processing item ID: 12345")

# Log errors
try:
    # Some operation
    result = 10 / 0
except Exception as e:
    logger.write_error_log(f"Error occurred: {str(e)}")
```

### TelegramBot Example

```python
from tgbot import TelegramBot

# Create a bot instance
bot = TelegramBot(token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

# Send notification
bot.send_message("✅ Application started successfully")
```

### FuturesAPIDecorator Example

```python
from futures_decorator import FuturesAPIDecorator
from CryptoAPI.futures.binance_api import BinanceFutures

# Create decorated API
binance = BinanceFutures()
trading_api = FuturesAPIDecorator(
    api=binance,
    token="YOUR_BOT_TOKEN", 
    chat_id="YOUR_CHAT_ID"
)

# Execute trade with automatic logging and notification
trading_api.place_market_order("BTC/USDT", "LONG", 5, 100.0)
```

For comprehensive documentation and advanced usage examples, please refer to the detailed README files for each utility:
- [ConfigReader Documentation](./documentation/config_reader_README.md)
- [Logger Documentation](./documentation/logger_README.md)
- [TelegramBot Documentation](./documentation/tgbot_README.md)
- [FuturesAPIDecorator Documentation](./documentation/futures_decorator_README.md)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](./LICENSE) file for details.

Copyright (c) 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
