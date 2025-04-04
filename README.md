# General Utilities

A collection of utility modules for common development tasks in Python applications.

## Available Utilities

### ConfigReader
A flexible configuration management utility that allows you to:
- Read configuration values from environment variables (.env files)
- Parse INI configuration files with automatic type conversion
- Retrieve individual settings or entire configuration sections
- Access configuration with a clean, consistent API

[View detailed ConfigReader documentation](./documentation/config_reader_README.md)

### Logger
A robust logging utility with advanced features:
- Write timestamped log messages to rotating daily files
- Separate general logs from error logs
- Full timezone support for accurate timestamps across different regions
- Handle various time formats (timestamps, datetime objects, string dates)
- Configurable log retention policies

[View detailed Logger documentation](./documentation/logger_README.md)

## Installation

### Using pip

```bash
# Install directly
pip install python-dotenv pytz

# Or install from requirements.txt
pip install -r requirements.txt
```

A `requirements.txt` file is included in the repository for easy installation of dependencies.

## Quick Start

### ConfigReader Example

```python
from config_reader import ConfigReader

# Initialize with default paths (.env and config.ini)
config = ConfigReader()

# Read from environment variables
api_key = config.get_env("API_KEY")
debug_mode = config.get_env("DEBUG_MODE", "False")

# Read typed values from config.ini
max_retries = config.get_config("network", "max_retries")  # Returns as int
timeout = config.get_config("network", "timeout")  # Returns as float

# Get an entire configuration section as a dictionary
database_config = config.get_config_section("database")
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

For comprehensive documentation and advanced usage examples, please refer to the detailed README files for each utility:
- [ConfigReader Documentation](./documentation/config_reader_README.md)
- [Logger Documentation](./documentation/logger_README.md)

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
