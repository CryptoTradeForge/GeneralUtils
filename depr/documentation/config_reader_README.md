# ConfigReader

A utility for reading configuration from environment variables and YAML files.

## Features

- Read values from environment variables
- Read values from YAML configuration files
- Support for nested configuration structures
- Get entire configuration sections as dictionaries
- Retrieve all environment variables or configuration values
- Fallback to default values when configuration is missing

## Installation

### Dependencies

This utility requires the `python-dotenv` and `PyYAML` packages.

```bash
# Install directly
pip install python-dotenv PyYAML

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

# Get config values
max_retries = config.get_config("app", "max_retries")
timeout = config.get_config("app", "timeout")

# Access nested configuration
db_host = config.get_config("database", "connection", "host")
db_port = config.get_config("database", "connection", "port")

# Get entire sections
app_config = config.get_config_section("app")
db_config = config.get_config_section("database")
```

### Example config.yaml File

```yaml
app:
  name: My Application
  version: 1.0.0
  max_retries: 3
  timeout: 5.5
  debug: true

database:
  connection:
    host: localhost
    port: 3306
    username: admin
    password: password123
  pool:
    max_connections: 10
    timeout: 30

features:
  dark_mode: true
  notifications: true
  auto_update: false
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
    env_path=".custom.env",          # Custom .env file path
    config_path="custom_config.yaml" # Custom config file path
)

# Or skip loading .env file
config_only = ConfigReader(env_path=None, config_path="config.yaml")

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
# Get all values in a section
database_config = config.get_config_section("database")
print(database_config)
# Output: {'connection': {'host': 'localhost', 'port': 3306, ...}, 'pool': {...}}

# Access nested values
connection = database_config.get("connection", {})
host = connection.get("host")
port = connection.get("port")
```

### Getting the Entire Configuration

```python
# Get the entire config file as a dictionary
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

- `ConfigReader(env_path=".env", config_path="config.yaml")` - Initialize with custom paths

### Methods

- `get_env(key, default=None)` - Get a value from environment variables
- `get_all_env(keys=None)` - Get multiple environment variables as a dictionary
- `get_config(*keys, default=None)` - Get a value from the config file with nested key support
- `get_config_section(section)` - Get an entire section from the config file
- `get_all_config()` - Get the entire config file as a dictionary
- `reload()` - Reload the configuration from the YAML file

### Nested Configuration Access

The ConfigReader supports access to deeply nested structures in YAML:

```python
# Access multi-level nested configuration
log_level = config.get_config("logging", "console", "level")
max_conn = config.get_config("database", "pool", "max_connections")
```
