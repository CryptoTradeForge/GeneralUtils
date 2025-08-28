# TelegramBot

A simple utility for sending notification messages through Telegram Bot API.

## Features

- Send text messages to specified Telegram chat IDs
- Easy integration with other applications
- Simple API with minimal dependencies
- Error handling for API communication issues
- Asynchronous message sending with synchronous wrapper

## Installation

### Dependencies

This utility requires the `python-telegram-bot` package.

```bash
# Install directly
pip install python-telegram-bot

# Or install from requirements.txt (recommended)
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from tgbot import TelegramBot

# Create a bot instance with your token and chat ID
bot = TelegramBot(
    token="YOUR_TELEGRAM_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID"
)

# Send a simple message
bot.send_message("Hello from my application!")

# Send a status update
bot.send_message("✅ Task completed successfully")

# Send an error notification
bot.send_message("❌ Error: Database connection failed")
```

### Getting Your Bot Token and Chat ID

1. **Bot Token**: 
   - Talk to the [BotFather](https://t.me/BotFather) on Telegram
   - Create a new bot using the `/newbot` command
   - Copy the token provided by BotFather

2. **Chat ID**:
   - Start a conversation with your bot
   - Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for the `"chat":{"id":123456789}` value in the response

### Handling Errors

```python
try:
    # Some operation that might fail
    result = process_data()
    bot.send_message(f"✅ Data processed successfully: {result}")
except Exception as e:
    # Send error notification via Telegram
    bot.send_message(f"❌ Error processing data: {str(e)}")
```

### Integration with Logger

```python
from logger import Logger
from tgbot import TelegramBot

# Create instances
logger = Logger()
bot = TelegramBot(token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

# Function that uses both
def process_task(task_id):
    try:
        logger.write_log(f"Starting task: {task_id}")
        # Process task...
        logger.write_log(f"Task {task_id} completed")
        bot.send_message(f"✅ Task {task_id} completed successfully")
    except Exception as e:
        error_msg = f"Error processing task {task_id}: {str(e)}"
        logger.write_error_log(error_msg)
        bot.send_message(f"❌ {error_msg}")
```

## API Reference

### Constructor

- `TelegramBot(token=None, chat_id=None)` - Initialize with your bot credentials
  - `token`: Your Telegram Bot API token (required)
  - `chat_id`: Default chat ID to send messages to (required)

### Methods

- `send_message(message)` - Send a text message to the default chat ID
  - `message`: The text message to send (required)

### Error Handling

The `send_message` method will raise exceptions in the following cases:
- Missing token or chat ID when initializing the bot
- Network errors when communicating with Telegram API
- API errors returned by Telegram

Best practice is to wrap your `send_message` calls in try-except blocks when reliability is critical.
