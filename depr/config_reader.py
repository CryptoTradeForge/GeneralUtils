# -*- coding: utf-8 -*-
"""
Config Reader Module - A utility for reading configuration from environment variables and YAML files
"""
import os
import yaml
from typing import Any, Dict, Optional, List, Union
from dotenv import load_dotenv

class ConfigReader:
    """
    A utility class for reading configuration from environment variables and YAML files.
    """
    
    def __init__(self, env_path: Optional[str] = ".env", config_path: Optional[str] = "config.yaml"):
        """
        Initialize the ConfigReader.
        
        Args:
            env_path: Path to the .env file. Set to None to skip loading .env file.
            config_path: Path to the config.yaml file. Set to None to skip loading config file.
        """
        self.config_data = {}
        self.config_path = config_path
        
        # Load environment variables if env_path is provided
        if env_path:
            load_dotenv(env_path)
        
        # Load config file if config_path is provided
        if config_path and os.path.exists(config_path):
            self._load_yaml_config()
    
    def _load_yaml_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self.config_data = yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            self.config_data = {}
        except Exception as e:
            print(f"Error loading config file: {e}")
            self.config_data = {}
    
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
    
    def get_config(self, *keys, default: Any = None) -> Any:
        """
        Get a value from the config.yaml file with nested key support.
        
        Args:
            *keys: Key path to access nested values (e.g., 'database', 'connection', 'host')
            default: Default value if the key path doesn't exist
            
        Returns:
            The value from the config or the default
        """
        if not keys:
            return default
        
        current = self.config_data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    def get_config_section(self, section: str) -> Dict[str, Any]:
        """
        Get an entire section from the config file as a dictionary.
        
        Args:
            section: The top-level key in the YAML file
            
        Returns:
            Dictionary containing all nested values in the section
        """
        return self.config_data.get(section, {})
    
    def get_all_config(self) -> Dict[str, Any]:
        """
        Get the entire config file as a dictionary.
        
        Returns:
            Dictionary containing all configuration values
        """
        return self.config_data
    
    def reload(self) -> None:
        """
        Reload the configuration from the YAML file.
        Useful when the file contents might have changed.
        """
        if self.config_path and os.path.exists(self.config_path):
            self._load_yaml_config()
