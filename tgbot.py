import os
import logging
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

class TelegramBot:
    """
    Telegram Bot framework for sending notifications.
    Uses provided token and chat_id or falls back to environment variables 
    TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.
    
    Note: This implementation currently only supports sending messages, 
    not receiving or responding to incoming messages.
    """
    
    def __init__(self, token: str = None, chat_id: str = None):
        """
        Initialize the TelegramBot.
        
        Args:
            token: The Telegram Bot token. If None, will try to read from environment variable.
            chat_id: Default chat ID to send messages to. If None, will try to read from environment variable.
            
        Note: The current implementation only initializes the bot for sending messages.
        Message receiving functionality is not implemented yet.
        """
        
        self.token = token
        self.chat_id = chat_id
        
        if not self.token:
            raise ValueError("Telegram Bot token not provided and TELEGRAM_BOT_TOKEN not found in environment variables")
        
        if not self.chat_id:
            raise ValueError("Telegram chat ID not provided and TELEGRAM_CHAT_ID not found in environment variables")

    async def _send_message_async(self, message: str):
        """
        Asynchronously sends a Telegram message to the default chat_id.
        
        This is part of the message sending functionality. Message receiving
        is not implemented.
        """
        bot = Bot(token=self.token)
        await bot.send_message(chat_id=self.chat_id, text=message)
    
    def send_message(self, message: str):
        """
        Sends a Telegram message to the default chat_id.
        
        This is the main public method for sending messages. The bot currently
        only supports sending messages, not receiving them.
        """
        asyncio.run(self._send_message_async(message))