import json
import logging
from io import StringIO
from typing import Any, Dict

import pytest

from mcp_pokemon.api.logging import JSONFormatter, LoggerContext, setup_logging

@pytest.fixture
def string_stream():
    """Create a string stream for capturing log output"""
    return StringIO()

@pytest.fixture
def json_logger(string_stream):
    """Create a logger with JSON formatting"""
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Create handler with string stream
    handler = logging.StreamHandler(string_stream)
    formatter = JSONFormatter(service="test-service", environment="test")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def get_log_entry(stream: StringIO) -> Dict[str, Any]:
    """Parse the last log entry from the stream"""
    return json.loads(stream.getvalue().strip().split("\n")[-1])

def test_json_formatter(json_logger, string_stream):
    """Test that logs are properly formatted as JSON"""
    json_logger.info("Test message", extra={"test_field": "test_value"})
    
    log_entry = get_log_entry(string_stream)
    
    assert log_entry["message"] == "Test message"
    assert log_entry["level"] == "INFO"
    assert log_entry["service"] == "test-service"
    assert log_entry["environment"] == "test"
    assert log_entry["test_field"] == "test_value"
    assert "timestamp" in log_entry

def test_logger_context(json_logger, string_stream):
    """Test that LoggerContext properly manages contextual log fields"""
    with LoggerContext(json_logger, request_id="123", user_id="456") as logger:
        logger.info("Test with context")
    
    json_logger.info("Test without context")
    
    log_entries = string_stream.getvalue().strip().split("\n")
    with_context = json.loads(log_entries[0])
    without_context = json.loads(log_entries[1])
    
    assert with_context["request_id"] == "123"
    assert with_context["user_id"] == "456"
    assert "request_id" not in without_context
    assert "user_id" not in without_context

def test_nested_logger_context(json_logger, string_stream):
    """Test nested LoggerContext behavior"""
    with LoggerContext(json_logger, outer="outer_value") as outer_logger:
        outer_logger.info("Outer context")
        
        with LoggerContext(outer_logger, inner="inner_value") as inner_logger:
            inner_logger.info("Inner context")
        
        outer_logger.info("Back to outer")
    
    log_entries = string_stream.getvalue().strip().split("\n")
    outer_log = json.loads(log_entries[0])
    inner_log = json.loads(log_entries[1])
    back_to_outer = json.loads(log_entries[2])
    
    assert outer_log["outer"] == "outer_value"
    assert "inner" not in outer_log
    
    assert inner_log["outer"] == "outer_value"
    assert inner_log["inner"] == "inner_value"
    
    assert back_to_outer["outer"] == "outer_value"
    assert "inner" not in back_to_outer

def test_exception_logging(json_logger, string_stream):
    """Test that exceptions are properly logged"""
    try:
        raise ValueError("Test error")
    except ValueError:
        json_logger.error("Error occurred", exc_info=True)
    
    log_entry = get_log_entry(string_stream)
    
    assert log_entry["level"] == "ERROR"
    assert log_entry["message"] == "Error occurred"
    assert log_entry["exception"]["type"] == "ValueError"
    assert log_entry["exception"]["message"] == "Test error"
    assert "traceback" in log_entry["exception"]

def test_setup_logging():
    """Test logging setup function"""
    # Capture initial handlers
    root_logger = logging.getLogger()
    initial_handlers = root_logger.handlers.copy()
    
    try:
        setup_logging(
            level="DEBUG",
            service_name="test-service",
            environment="test"
        )
        
        # Verify logger configuration
        assert root_logger.level == logging.DEBUG
        assert len(root_logger.handlers) == 1
        
        handler = root_logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        assert isinstance(handler.formatter, JSONFormatter)
        
    finally:
        # Restore initial handlers
        root_logger.handlers = initial_handlers 