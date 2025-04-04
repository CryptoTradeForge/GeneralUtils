# -*- coding: utf-8 -*-
"""
Config Reader Module - A utility for reading configuration from environment variables and INI files
"""
import os
import configparser
from typing import Any, Dict, Optional, List, Union
from dotenv import load_dotenv

class ConfigReader:
    """
    A utility class for reading configuration from environment variables and INI files.
    """
    
    def __init__(self, env_path: Optional[str] = ".env", config_path: Optional[str] = "config.ini"):
        """
        Initialize the ConfigReader.
        
        Args:
            env_path: Path to the .env file. Set to None to skip loading .env file.
            config_path: Path to the config.ini file. Set to None to skip loading config file.
        """
        self.config_parser = configparser.ConfigParser()
        self.config_path = config_path
        
        # Load environment variables if env_path is provided
        if env_path:
            load_dotenv(env_path)
        
        # Load config file if config_path is provided
        if config_path and os.path.exists(config_path):
            self.config_parser.read(config_path, encoding="utf-8")
    
    def get_env(self, key: str, default: Any = None) -> Any:
        """
        Get a value from environment variables.
        
        Args:
            key: The environment variable name
            default: Default value if the key doesn't exist
            
        Returns:
            The value of the environment variable or the default
        """
        return os.getenv(key, default)
    
    def get_all_env(self, keys: List[str] = None) -> Dict[str, str]:
        """
        Get multiple environment variables as a dictionary.
        
        Args:
            keys: List of environment variable names to retrieve.
                If None, returns all environment variables.
            
        Returns:
            Dictionary of environment variables
        """
        if keys is None:
            return dict(os.environ)
        
        return {key: os.getenv(key) for key in keys if os.getenv(key) is not None}
    
    def _convert_value_type(self, value: str) -> Any:
        """
        Convert string value to appropriate type (int, float, bool, or string).
        
        Args:
            value: String value to convert
            
        Returns:
            Converted value with appropriate type
        """
        # Try converting to int
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try converting to float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Check for boolean values
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False
        
        # Return as string if no conversion applies
        return value
    
    def get_config(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a value from the config.ini file with automatic type conversion.
        
        Args:
            section: The section in the INI file
            key: The key in the section
            default: Default value if the section/key doesn't exist
            
        Returns:
            The value from the config (with appropriate type) or the default
        """
        try:
            value = self.config_parser.get(section, key)
            return self._convert_value_type(value)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default
    
    def get_config_section(self, section: str) -> Dict[str, Any]:
        """
        Get an entire section from the config file as a dictionary with typed values.
        
        Args:
            section: The section name in the INI file
            
        Returns:
            Dictionary containing all keys/values in the section with appropriate types
        """
        try:
            if section in self.config_parser:
                return {key: self._convert_value_type(value) 
                        for key, value in self.config_parser[section].items()}
            return {}
        except (configparser.NoSectionError, KeyError):
            return {}
    
    def get_all_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the entire config file as a nested dictionary with typed values.
        
        Returns:
            Dictionary where keys are section names and values are
            dictionaries of key/value pairs in each section
        """
        return {section: self.get_config_section(section) 
                for section in self.config_parser.sections()}
    
    def reload(self) -> None:
        """
        Reload the configuration from the ini file.
        Useful when the file contents might have changed.
        """
        if self.config_path and os.path.exists(self.config_path):
            self.config_parser = configparser.ConfigParser()
            self.config_parser.read(self.config_path, encoding="utf-8")
