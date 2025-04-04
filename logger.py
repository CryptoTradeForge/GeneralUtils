# -*- coding: utf-8 -*-
"""
Logger Module - A utility for logging general and error messages with timezone support
"""
import pytz
import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


class Logger:
    """
    A class-based logger with timezone support.
    """
    
    def __init__(self, log_dir=None, timezone_str="Asia/Taipei", backup_count=30):
        """
        Initialize the logger with specified configuration.
        
        Args:
            log_dir (str, optional): Base directory for log files. If None, current directory is used.
            timezone_str (str, optional): Timezone string. Defaults to "Asia/Taipei".
            backup_count (int, optional): Number of backup log files to keep. Defaults to 30.
        """
        self.timezone = pytz.timezone(timezone_str)
        self.backup_count = backup_count
        
        # Set up log directories
        if log_dir is None:
            log_dir = os.path.join(os.getcwd(), "logs")
        
        self.general_log_folder = os.path.join(log_dir, "general_logs")
        self.error_log_folder = os.path.join(log_dir, "error_logs")
        
        # Create log directories if they don't exist
        os.makedirs(self.general_log_folder, exist_ok=True)
        os.makedirs(self.error_log_folder, exist_ok=True)
        
        # Initialize loggers
        self.general_logger = self._setup_general_logger()
        self.error_logger = self._setup_error_logger()
    
    class TimezoneFormatter(logging.Formatter):
        """Custom formatter with timezone support"""
        
        def __init__(self, fmt, timezone):
            super().__init__(fmt)
            self.timezone = timezone
            
        def converter(self, timestamp):
            dt = datetime.fromtimestamp(timestamp, tz=pytz.utc)
            return dt.astimezone(self.timezone)
    
        def formatTime(self, record, datefmt=None):
            dt = self.converter(record.created)
            if datefmt:
                return dt.strftime(datefmt)
            return dt.isoformat()
    
    def _setup_general_logger(self):
        """Configure and return the general logger"""
        logger = logging.getLogger("general_logger")
        
        if not logger.hasHandlers():
            handler = TimedRotatingFileHandler(
                filename=os.path.join(self.general_log_folder, "general.log"),
                when="midnight",
                interval=1,
                backupCount=self.backup_count,
                encoding="utf-8"
            )
            handler.suffix = "%Y-%m-%d"
            handler.setFormatter(self.TimezoneFormatter("%(message)s", self.timezone))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        
        return logger
    
    def _setup_error_logger(self):
        """Configure and return the error logger"""
        logger = logging.getLogger("error_logger")
        
        if not logger.hasHandlers():
            handler = TimedRotatingFileHandler(
                filename=os.path.join(self.error_log_folder, "error.log"),
                when="midnight",
                interval=1,
                backupCount=self.backup_count,
                encoding="utf-8"
            )
            handler.suffix = "%Y-%m-%d"
            handler.setFormatter(self.TimezoneFormatter("%(message)s", self.timezone))
            logger.addHandler(handler)
            logger.setLevel(logging.ERROR)
        
        return logger
    
    def _format_time(self, time_input=None):
        """
        Format time input to a standardized string format.
        
        Args:
            time_input: Time input in various formats (timestamp, string, datetime object)
                        or None for current time
        
        Returns:
            str: Formatted time string in the format '%Y-%m-%d %H:%M:%S'
        """
        if time_input is None:
            # Use current time
            return datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')
        
        # If already a formatted string in the correct format
        if isinstance(time_input, str):
            # Check if it's already in the correct format
            if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', time_input):
                return time_input
            
            # Try to parse the string as a datetime
            try:
                dt = datetime.fromisoformat(time_input.replace('Z', '+00:00'))
                return dt.astimezone(self.timezone).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                # Not a standard datetime string format
                pass
        
        # If it's a datetime object
        if isinstance(time_input, datetime):
            # Ensure it has timezone info
            if time_input.tzinfo is None:
                time_input = time_input.replace(tzinfo=pytz.utc)
            return time_input.astimezone(self.timezone).strftime('%Y-%m-%d %H:%M:%S')
        
        # If it's a timestamp (int or float)
        if isinstance(time_input, (int, float)):
            # Check if it's milliseconds (large number)
            if time_input > 1e10:  # Threshold for determining milliseconds timestamp
                time_input /= 1000  # Convert milliseconds to seconds
            
            dt = datetime.fromtimestamp(time_input, tz=pytz.utc)
            return dt.astimezone(self.timezone).strftime('%Y-%m-%d %H:%M:%S')
            
        
        raise ValueError("Unsupported time format. Please provide a timestamp, string, or datetime object.")
    
    def write_log(self, message, time=None):
        """
        Write a message to the general log.
        
        Args:
            message (str): The message to log
            time: Custom timestamp for the log in various formats. 
                If None, current time is used.
        """
        try:
            formatted_time = self._format_time(time)
        except ValueError as e:
            # Use direct logger access to avoid recursion
            warning_time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')
            self.write_error_log(f"[WARNING] Invalid time format in write_log: {time}. Using current time instead.", time=warning_time)
            formatted_time = warning_time
            
        log_message = f"[{formatted_time}] {message}"
        self.general_logger.info(log_message)
    
    def write_error_log(self, message, time=None):
        """
        Write a message to the error log.
        
        Args:
            message (str): The error message to log
            time: Custom timestamp for the error in various formats.
                If None, current time is used.
        """
        try:
            formatted_time = self._format_time(time)
        except ValueError as e:
            # Use direct logger access to avoid recursion
            warning_time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')
            self.write_error_log(f"[WARNING] Invalid time format in write_error_log: {time}. Using current time instead.", time=warning_time)
            formatted_time = warning_time
            
        log_message = f"[{formatted_time}] {message}"
        self.error_logger.error(log_message)

