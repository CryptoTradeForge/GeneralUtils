# General Utilities

A collection of essential utility modules for cryptocurrency trading applications and general Python development.

## Available Utilities

### Logger
A modern logging utility with advanced features:
- Rotating file handlers with configurable size limits and backup counts
- Timezone-aware timestamping with pytz support
- Colored console output for different log levels
- Flexible log level configuration for both file and stream handlers
- UTF-8 encoding support for international characters
- Clean, customizable formatting for both file and console output

### TelegramBot
A lightweight utility for sending Telegram notifications:
- Asynchronous message sending with simple synchronous interface
- Direct token and chat_id configuration
- Clean error handling for API communication
- Minimal dependencies for easy integration
- Perfect for trading alerts and system notifications

### ExclusionCoinsRecord
A specialized utility for cryptocurrency trading symbol management:
- Manage lists of stable coins and problematic trading pairs
- Automatic symbol filtering for trading strategies
- JSON-based persistence for exclusion lists
- Smart symbol handling (automatic USDT suffix management)
- Easy integration with trading algorithms

## Installation

### Using pip

```bash
# Install dependencies
pip install pytz python-telegram-bot

# Or install from requirements.txt
pip install -r requirements.txt
```

## Quick Start

### Logger Example

```python
from GeneralUtils import set_logger
import logging

# Create a logger with file output and colored console
logger = set_logger(
    name="my_app",
    filepath="logs/app.log",
    file_log_level=logging.DEBUG,
    stream_log_level=logging.INFO,
    timezone="Asia/Taipei"
)

# Use the logger
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
logger.debug("Debug information")
```

### TelegramBot Example

```python
from GeneralUtils import TelegramBot

# Create a bot instance
bot = TelegramBot(token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

# Send notifications
bot.send_message("🚀 Trading bot started")
bot.send_message("📈 Position opened: BTC/USDT LONG")
bot.send_message("✅ Trade completed successfully")
```

### ExclusionCoinsRecord Example

```python
from GeneralUtils import ExclusionCoinsRecord

# Initialize exclusion manager
exclusion = ExclusionCoinsRecord("data/exclusion_coins.json")

# Add coins to exclusion lists
exclusion.add_stable_coin("USDC")
exclusion.add_problematic_coin("HYPE")

# Filter trading symbols
all_symbols = ["BTCUSDT", "ETHUSDT", "USDCUSDT", "HYPEUSDT", "ADAUSDT"]
filtered_symbols = exclusion.filter_symbols(all_symbols)
print(filtered_symbols)  # ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']

# Get exclusion lists
stable_coins = exclusion.get_stable_coins()
problematic_coins = exclusion.get_problematic_coins()
all_excluded = exclusion.get_exclusion_coins()
```

## File Structure

```
libs/GeneralUtils/
├── __init__.py              # Package initialization and exports
├── logger.py                # Advanced logging with timezone support
├── tgbot.py                 # Telegram notification utility
├── exclusion_coins_record.py # Cryptocurrency symbol filtering
├── exclusion_coins_example.json # Example exclusion configuration
├── requirements.txt         # Package dependencies
├── LICENSE                  # Apache 2.0 License
└── README.md               # This file
```

## Key Features

- **Modular Design**: Each utility is independent and can be used separately
- **Cryptocurrency Trading Focus**: Specialized tools for trading applications
- **Production Ready**: Robust error handling and logging
- **Easy Integration**: Simple APIs with sensible defaults
- **Timezone Support**: Full timezone awareness for global trading
- **Notification System**: Real-time Telegram alerts for trading events

## Advanced Usage

### Logger with Custom Configuration

```python
from GeneralUtils import set_logger
import logging

# Create logger with custom settings
logger = set_logger(
    name="trading_bot",
    filepath="logs/trading.log",
    file_log_level=logging.DEBUG,      # Log everything to file
    stream_log_level=logging.WARNING,  # Only warnings+ to console
    max_bytes=10 * 1024 * 1024,       # 10MB per log file
    backup_count=5,                    # Keep 5 backup files
    timezone="UTC"                     # Use UTC timezone
)

# The logger automatically handles:
# - File rotation when size limit is reached
# - Colored output in console
# - Timezone-aware timestamps
# - UTF-8 encoding for international characters
```

### ExclusionCoinsRecord Advanced Features

```python
from GeneralUtils import ExclusionCoinsRecord

# Initialize with custom path
exclusion = ExclusionCoinsRecord("custom/path/exclusions.json")

# Bulk operations
symbols_to_check = ["BTCUSDT", "ETHUSDT", "USDCUSDT", "DOGEUSDT"]
clean_symbols = exclusion.filter_symbols(symbols_to_check)

# The system automatically:
# - Handles USDT suffix normalization
# - Persists changes to JSON file
# - Prevents duplicate entries
# - Maintains separate stable/problematic lists
```

### Integration Example: Trading Bot with Full Logging and Notifications

```python
from GeneralUtils import set_logger, TelegramBot, ExclusionCoinsRecord
import logging

# Setup comprehensive logging
logger = set_logger(
    name="crypto_trader",
    filepath="logs/trader.log",
    timezone="Asia/Taipei"
)

# Setup notifications
bot = TelegramBot(token="YOUR_TOKEN", chat_id="YOUR_CHAT_ID")

# Setup symbol filtering
exclusion = ExclusionCoinsRecord()

class TradingBot:
    def __init__(self):
        self.logger = logger
        self.notifications = bot
        self.symbol_filter = exclusion
    
    def start_trading(self):
        self.logger.info("🚀 Trading bot initialization started")
        self.notifications.send_message("🚀 Trading bot started")
        
        # Get and filter symbols
        all_symbols = self.get_available_symbols()
        filtered_symbols = self.symbol_filter.filter_symbols(all_symbols)
        
        self.logger.info(f"📊 Filtered {len(all_symbols)} symbols to {len(filtered_symbols)}")
```

## Dependencies

- **pytz** (>=2021.1): Timezone handling for global trading applications
- **python-telegram-bot** (>=20.0): Telegram API integration for notifications

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
