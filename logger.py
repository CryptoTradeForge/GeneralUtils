import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional, Union
import pytz
from datetime import datetime

# 彩色輸出輔助
LEVEL_COLORS = {
    "DEBUG": "\033[37m",    # 白色
    "INFO": "\033[32m",     # 綠色
    "WARNING": "\033[33m",  # 黃色
    "ERROR": "\033[31m",    # 紅色
    "CRITICAL": "\033[35m", # 紫色
}
RESET_COLOR = "\033[0m"

class TimezoneFormatter(logging.Formatter):
    """支援時區的 Formatter"""
    def __init__(self, fmt=None, datefmt=None, timezone=None):
        super().__init__(fmt, datefmt)
        self.timezone = timezone
    
    def formatTime(self, record, datefmt=None):
        if self.timezone:
            dt = datetime.fromtimestamp(record.created, tz=self.timezone)
        else:
            dt = datetime.fromtimestamp(record.created)
        
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.strftime('%Y-%m-%d %H:%M:%S')

class ColoredFormatter(TimezoneFormatter):
    def format(self, record):
        levelname = record.levelname
        color = LEVEL_COLORS.get(levelname, "")
        record.levelname = f"{color}[{levelname}]{RESET_COLOR}"
        return super().format(record)

def set_logger(
    name: str,
    filepath: Optional[str] = None,
    file_log_level: int = logging.DEBUG,
    stream_log_level: int = logging.WARNING,
    log_level: int = logging.DEBUG,
    max_bytes: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 3,
    timezone: Optional[Union[str, pytz.BaseTzInfo]] = None
) -> logging.Logger:
    
    # 步驟 1: 設定 logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.handlers.clear()  # 清除現有 handlers

    # 處理時區參數
    tz = None
    if timezone:
        if isinstance(timezone, str):
            # 如果是字符串，轉換為 pytz 時區對象
            tz = pytz.timezone(timezone)
        elif isinstance(timezone, pytz.BaseTzInfo):
            # 如果已經是 pytz 時區對象，直接使用
            tz = timezone
        else:
            raise ValueError(f"timezone 必須是字符串或 pytz.BaseTzInfo 物件，收到: {type(timezone)}")

    # --- File 格式（詳細） ---
    file_formatter = TimezoneFormatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        timezone=tz
    )

    # --- Stream 格式（彩色 [LEVEL] + message） ---
    stream_formatter = ColoredFormatter(
        '%(levelname)s %(message)s',
        timezone=tz
    )

    # 步驟 2: 檔案 handler
    if filepath is not None:
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath, exist_ok=True)
        file_handler = RotatingFileHandler(
            filepath,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # 步驟 3: Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_log_level)
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger
