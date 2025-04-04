# ConfigReader

A utility for reading configuration from environment variables and INI files.

## Features

- Read values from environment variables
- Read values from INI configuration files with automatic type conversion
- Get entire configuration sections as dictionaries
- Retrieve all environment variables or configuration values
- Support for different data types (int, float, boolean, string)
- Fallback to default values when configuration is missing

## Installation

### Dependencies

This utility requires the `python-dotenv` package.

```bash
# Install directly
pip install python-dotenv

# Or install from requirements.txt (recommended)
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from config_reader import ConfigReader

# Create a config reader instance with default settings
config = ConfigReader()

# Get environment variables
api_key = config.get_env("API_KEY")
debug_mode = config.get_env("DEBUG_MODE", "False")  # With default value

# Get config values with auto type conversion
max_retries = config.get_config("app", "max_retries")  # Returns integer
timeout = config.get_config("app", "timeout")  # Returns float
is_enabled = config.get_config("features", "dark_mode")  # Returns boolean
app_name = config.get_config("app", "name")  # Returns string

# Get entire sections
app_config = config.get_config_section("app")
db_config = config.get_config_section("database")
```

### Example config.ini File

```ini
[app]
name = My Application
version = 1.0.0
max_retries = 3
timeout = 5.5
debug = true

[database]
host = localhost
port = 3306
username = admin
password = password123
max_connections = 10

[features]
dark_mode = true
notifications = true
auto_update = false
```

### Example .env File

```
API_KEY=your_secret_api_key_here
DEBUG_MODE=true
DB_PASSWORD=secure_password
```

### Using with Custom Configuration Paths

```python
custom_config = ConfigReader(
    env_path=".custom.env",         # Custom .env file path
    config_path="custom_config.ini" # Custom config file path
)

# Or skip loading .env file
config_only = ConfigReader(env_path=None, config_path="config.ini")

# Or skip loading config file
env_only = ConfigReader(env_path=".env", config_path=None)
```

### Working with Multiple Environment Variables

```python
# Get specific environment variables as a dictionary
db_env_vars = config.get_all_env(["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD"])
print(db_env_vars)  # {'DB_HOST': 'localhost', 'DB_PORT': '5432', ...}

# Get all environment variables
all_env_vars = config.get_all_env()
```

### Working with Configuration Sections

```python
# Get all values in a section with proper types
database_config = config.get_config_section("database")
print(database_config)  
# Output: {'host': 'localhost', 'port': 3306, 'username': 'admin', ...}

# Access values from the dictionary
host = database_config["host"]
port = database_config["port"]  # This is an integer!
```

### Getting the Entire Configuration

```python
# Get the entire config file as a nested dictionary
all_configs = config.get_all_config()
print(all_configs)
# Output: {'app': {'name': 'My Application', ...}, 'database': {...}, ...}
```

### Reloading Configuration

```python
# Reload config from disk (useful if the config file has been modified)
config.reload()
```

## API Reference

### Constructor

- `ConfigReader(env_path=".env", config_path="config.ini")` - Initialize with custom paths

### Methods

- `get_env(key, default=None)` - Get a value from environment variables
- `get_all_env(keys=None)` - Get multiple environment variables as a dictionary
- `get_config(section, key, default=None)` - Get a value from the config file with type conversion
- `get_config_section(section)` - Get an entire section from the config file
- `get_all_config()` - Get the entire config file as a nested dictionary
- `reload()` - Reload the configuration from the ini file

### Type Conversion

The ConfigReader automatically converts string values from the config file to appropriate types:

- Integer values: `"42"` → `42`
- Float values: `"3.14"` → `3.14`
- Boolean values: 
  - `"true"`, `"yes"`, `"1"` → `True`
  - `"false"`, `"no"`, `"0"` → `False`
- Other values remain as strings
