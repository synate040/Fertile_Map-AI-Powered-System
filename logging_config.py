# ==================== LOGGING CONFIGURATION ====================
"""
Logging setup for FERTILE MAP backend
Provides structured logging for debugging and monitoring
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logging(app):
    """
    Setup logging configuration for the Flask app
    Creates logs directory if needed and configures both file and console logging
    """
    
    # Ensure logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Get log level from config
    log_level = getattr(app.config, 'LOG_LEVEL', 'INFO')
    log_file = getattr(app.config, 'LOG_FILE', os.path.join(log_dir, 'app.log'))
    
    # Create logger
    logger = logging.getLogger('fertile_map')
    logger.setLevel(getattr(logging, log_level))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # Log initial message
    logger.info(f"Logging initialized - Level: {log_level}")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Environment: {app.config.get('FLASK_ENV', 'development')}")
    
    return logger

def log_request(logger, method, path, status_code, duration):
    """Log HTTP request"""
    logger.info(f"REQUEST: {method} {path} - Status: {status_code} - Duration: {duration:.2f}ms")

def log_error(logger, error_type, message, exception=None):
    """Log error with optional exception traceback"""
    if exception:
        logger.error(f"{error_type}: {message}", exc_info=exception)
    else:
        logger.error(f"{error_type}: {message}")

def log_info(logger, message):
    """Log info message"""
    logger.info(message)

def log_warning(logger, message):
    """Log warning message"""
    logger.warning(message)

def log_debug(logger, message):
    """Log debug message"""
    logger.debug(message)

# Get or create logger
logger = logging.getLogger('fertile_map')
