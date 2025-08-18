import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

# 彩色輸出輔助
LEVEL_COLORS = {
    "DEBUG": "\033[37m",    # 白色
    "INFO": "\033[32m",     # 綠色
    "WARNING": "\033[33m",  # 黃色
    "ERROR": "\033[31m",    # 紅色
    "CRITICAL": "\033[35m", # 紫色
}
RESET_COLOR = "\033[0m"

class ColoredFormatter(logging.Formatter):
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
    backup_count: int = 3
) -> logging.Logger:
    
    # 步驟 1: 設定 logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.handlers.clear()  # 清除現有 handlers

    # --- File 格式（詳細） ---
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # --- Stream 格式（彩色 [LEVEL] + message） ---
    stream_formatter = ColoredFormatter(
        '%(levelname)s %(message)s'
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
