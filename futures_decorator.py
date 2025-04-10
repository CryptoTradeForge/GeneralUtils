from typing import Optional, List, Dict, Union, Any, Callable
import functools
import os
import traceback
import json

class FuturesAPIDecorator:
    """
    A decorator class for FuturesAPI implementations. 
    Adds logging and telegram notifications for trading actions.
    """
    
    # Methods requiring logging and notifications
    TRADING_METHODS = [
        'set_stop_loss_take_profit',
        'place_market_order',
        'place_limit_order',
        'close_position',
        'cancel_order'
    ]
    
    # Methods that just need to pass through without decoration
    INFO_METHODS = [
        'get_positions',
        'get_open_orders',
        'fetch_usdt_balance',
        'get_price',
        'get_historical_data'
    ]
    
    def __init__(self, api, logger=None, tgbot=None, log_dir=None, token=None, chat_id=None):
        """
        Initialize the decorator with a FuturesAPI instance.
        
        Args:
            api: An instance of a class implementing the AbstractFuturesAPI interface
            logger: Optional Logger instance. If None, a new Logger will be created
            tgbot: Optional TelegramBot instance. If None, a new TelegramBot will be created
            log_dir: Directory for logs (if logger is None)
            token: Telegram bot token (if tgbot is None)
            chat_id: Telegram chat ID (if tgbot is None)
        """
        self.api = api
        
        # Initialize logger
        if logger is None:
            from .logger import Logger
            self.logger = Logger(log_dir=log_dir)
        else:
            self.logger = logger
            
        # Initialize Telegram bot
        if tgbot is None and token and chat_id:
            from .tgbot import TelegramBot
            self.tgbot = TelegramBot(token=token, chat_id=chat_id)
        else:
            self.tgbot = tgbot
            
        # Dynamically decorate methods
        self._decorate_methods()
    
    def _log_and_notify(self, action: str, success: bool, details: Dict = None, error: Exception = None) -> None:
        """
        Log action and send notification via telegram.
        
        Args:
            action: Description of the action
            success: Whether the action was successful
            details: Additional details about the action
            error: Exception if an error occurred
        """
        status = "✅ SUCCESS" if success else "❌ ERROR"
        message = f"{status}: {action}"
        
        if details:
            detail_str = json.dumps(details, ensure_ascii=False)
            message += f"\nDetails: {detail_str}"
            
        if error:
            message += f"\nError: {str(error)}"
            self.logger.write_error_log(message)
        else:
            self.logger.write_log(message)
            
        # Send notification via telegram if available
        if self.tgbot:
            try:
                self.tgbot.send_message(message)
            except Exception as e:
                self.logger.write_error_log(f"Failed to send Telegram notification: {str(e)}")
    
    def _decorate_methods(self):
        """
        Dynamically decorate API methods based on their type.
        Trading methods get logging and notifications,
        Info methods are passed through directly.
        """
        for method_name in dir(self.api):
            # Skip private/special methods
            if method_name.startswith('_'):
                continue
                
            # Get the method
            method = getattr(self.api, method_name)
            if not callable(method):
                continue
                
            if method_name in self.TRADING_METHODS:
                # Decorate trading methods
                setattr(self, method_name, self._create_trading_decorator(method_name, method))
            elif method_name in self.INFO_METHODS:
                # Pass through info methods
                setattr(self, method_name, method)
            else:
                # For any other methods, just pass them through
                setattr(self, method_name, method)
    
    def _create_trading_decorator(self, method_name, method):
        """
        Create a decorator for trading methods that adds logging and notifications.
        
        Args:
            method_name: Name of the method being decorated
            method: The method function to decorate
            
        Returns:
            function: Decorated method
        """
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            # Extract relevant information for logging
            details = self._extract_details(method_name, args, kwargs)
            
            try:
                result = method(*args, **kwargs)
                action = self._get_success_message(method_name, args, kwargs)
                self._log_and_notify(action, True, details)
                return result
            except Exception as e:
                action = self._get_error_message(method_name, args, kwargs)
                self._log_and_notify(action, False, details, e)
                raise
        
        return wrapper
    
    def _extract_details(self, method_name, args, kwargs):
        """
        Extract relevant details for logging based on method name and arguments.
        
        Args:
            method_name: Name of the method
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            dict: Details for logging
        """
        details = {}
        
        # First argument after self is usually symbol
        if len(args) > 1:
            details["symbol"] = args[1]
        elif "symbol" in kwargs:
            details["symbol"] = kwargs["symbol"]
            
        # Extract other common parameters based on method name
        if method_name == "set_stop_loss_take_profit":
            if len(args) > 2:
                details["side"] = args[2]
            if len(args) > 3:
                details["quantity"] = args[3]
            if len(args) > 4:
                details["stop_loss"] = args[4]
            if len(args) > 5:
                details["take_profit"] = args[5]
                
            # Override with kwargs if present
            details.update({k: v for k, v in kwargs.items() if k in ["side", "quantity", "stop_loss_price", "take_profit_price"]})
            
        elif method_name in ["place_market_order", "place_limit_order"]:
            if len(args) > 2:
                details["position"] = args[2]
            if method_name == "place_limit_order" and len(args) > 3:
                details["price"] = args[3]
            if len(args) > (4 if method_name == "place_limit_order" else 3):
                details["leverage"] = args[4 if method_name == "place_limit_order" else 3]
            if len(args) > (5 if method_name == "place_limit_order" else 4):
                details["amount"] = args[5 if method_name == "place_limit_order" else 4]
                
            # Add stop loss and take profit for market orders
            if method_name == "place_market_order":
                if len(args) > 5:
                    details["stop_loss"] = args[5]
                if len(args) > 6:
                    details["take_profit"] = args[6]
                    
            # Override with kwargs if present
            details.update({k: v for k, v in kwargs.items() 
                          if k in ["position_type", "price", "leverage", "amount", "stop_loss_price", "take_profit_price"]})
                
        elif method_name == "close_position":
            if len(args) > 2:
                details["position"] = args[2]
            if "position_type" in kwargs:
                details["position"] = kwargs["position_type"]
                
        elif method_name == "cancel_order":
            if len(args) > 2:
                details["type"] = args[2]
            if "type" in kwargs:
                details["type"] = kwargs["type"]
                
        return details
    
    def _get_success_message(self, method_name, args, kwargs):
        """
        Generate a success message based on the method and arguments.
        
        Args:
            method_name: Name of the method
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            str: Success message
        """
        symbol = args[1] if len(args) > 1 else kwargs.get("symbol", "unknown")
        
        if method_name == "set_stop_loss_take_profit":
            side = args[2] if len(args) > 2 else kwargs.get("side", "unknown")
            return f"Set SL/TP for {symbol} ({side})"
            
        elif method_name == "place_market_order":
            position_type = args[2] if len(args) > 2 else kwargs.get("position_type", "unknown")
            return f"Placed market {position_type} order for {symbol}"
            
        elif method_name == "place_limit_order":
            position_type = args[2] if len(args) > 2 else kwargs.get("position_type", "unknown")
            price = args[3] if len(args) > 3 else kwargs.get("price", "unknown")
            return f"Placed limit {position_type} order for {symbol} at {price}"
            
        elif method_name == "close_position":
            position_type = args[2] if len(args) > 2 else kwargs.get("position_type", "unknown")
            return f"Closed {position_type} position for {symbol}"
            
        elif method_name == "cancel_order":
            order_type = args[2] if len(args) > 2 else kwargs.get("type", "")
            type_str = f" {order_type}" if order_type else ""
            return f"Cancelled{type_str} orders for {symbol}"
            
        return f"Executed {method_name} for {symbol}"
    
    def _get_error_message(self, method_name, args, kwargs):
        """
        Generate an error message based on the method and arguments.
        
        Args:
            method_name: Name of the method
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            str: Error message
        """
        symbol = args[1] if len(args) > 1 else kwargs.get("symbol", "unknown")
        
        if method_name == "set_stop_loss_take_profit":
            side = args[2] if len(args) > 2 else kwargs.get("side", "unknown")
            return f"Failed to set SL/TP for {symbol} ({side})"
            
        elif method_name == "place_market_order":
            position_type = args[2] if len(args) > 2 else kwargs.get("position_type", "unknown")
            return f"Failed to place market {position_type} order for {symbol}"
            
        elif method_name == "place_limit_order":
            position_type = args[2] if len(args) > 2 else kwargs.get("position_type", "unknown")
            return f"Failed to place limit {position_type} order for {symbol}"
            
        elif method_name == "close_position":
            position_type = args[2] if len(args) > 2 else kwargs.get("position_type", "unknown")
            return f"Failed to close {position_type} position for {symbol}"
            
        elif method_name == "cancel_order":
            order_type = args[2] if len(args) > 2 else kwargs.get("type", "")
            type_str = f" {order_type}" if order_type else ""
            return f"Failed to cancel{type_str} orders for {symbol}"
            
        return f"Failed to execute {method_name} for {symbol}"
