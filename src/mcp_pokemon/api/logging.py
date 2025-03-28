import json
import logging
from contextlib import contextmanager
from datetime import UTC, datetime
from typing import Any, Dict, Optional

class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs as JSON"""
    
    def __init__(self, service: str, environment: str):
        super().__init__()
        self.service = service
        self.environment = environment
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as JSON"""
        # Base log data
        log_data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "service": self.service,
            "environment": self.environment
        }
        
        # Add exception info if present
        if record.exc_info:
            exc_type, exc_value, exc_tb = record.exc_info
            log_data["exception"] = {
                "type": exc_type.__name__,
                "message": str(exc_value),
                "traceback": self.formatException(record.exc_info)
            }
        
        # Add extra fields from record
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # Add any additional attributes from the record
        for key, value in record.__dict__.items():
            if (
                key not in {
                    "args", "asctime", "created", "exc_info", "exc_text",
                    "filename", "funcName", "levelname", "levelno", "lineno",
                    "module", "msecs", "msg", "name", "pathname", "process",
                    "processName", "relativeCreated", "stack_info", "thread",
                    "threadName", "extra"
                }
                and not key.startswith("_")
            ):
                log_data[key] = value
        
        return json.dumps(log_data)

class LoggerAdapter(logging.LoggerAdapter):
    """Adapter that adds extra fields to log records"""
    
    def __init__(self, logger: logging.Logger, extra: Dict[str, Any]):
        # If logger is already an adapter, merge its extra fields
        if isinstance(logger, LoggerAdapter):
            extra = {**logger.extra, **extra}
            logger = logger.logger
        super().__init__(logger, extra or {})
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        """Process the logging message and keyword arguments"""
        kwargs.setdefault("extra", {}).update(self.extra)
        return msg, kwargs

@contextmanager
def LoggerContext(logger: logging.Logger, **context_fields: Any):
    """Context manager for adding temporary fields to log records"""
    if isinstance(logger, LoggerAdapter):
        # Create new adapter with merged fields
        new_extra = {**logger.extra, **context_fields}
        new_logger = LoggerAdapter(logger.logger, new_extra)
    else:
        # Create new adapter with context fields
        new_logger = LoggerAdapter(logger, context_fields)
    
    try:
        yield new_logger
    finally:
        pass

def setup_logging(
    level: str = "INFO",
    service_name: str = "mcp-pokemon",
    environment: str = "development"
) -> None:
    """Set up logging configuration"""
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Set log level
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Create console handler with JSON formatter
    console_handler = logging.StreamHandler()
    formatter = JSONFormatter(service=service_name, environment=environment)
    console_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name) 