"""
===============================================================================
File: constants.py

Purpose:
    Defines application-wide constants used throughout the project.

Business Problem:
    Hardcoded strings such as Redis keys, event names, JSON fields,
    and market statuses quickly become difficult to maintain as an
    application grows.

    This file centralizes those constants so every module references
    the same values.

Benefits:
    - Eliminates magic strings
    - Prevents typographical mistakes
    - Improves code readability
    - Makes future changes easier
    - Provides a single source of truth

Author:
    Kuldip Awachar

Repository:
    low-latency-market-data-engine-using-redis-python
===============================================================================
"""

# ==============================================================================
# Application Information
# ==============================================================================

APPLICATION_NAME: str = "Low Latency Market Data Engine"

APPLICATION_VERSION: str = "1.0.0"

# ==============================================================================
# Market Status
# ==============================================================================

MARKET_OPEN: str = "OPEN"
MARKET_CLOSED: str = "CLOSED"

# ==============================================================================
# Event Types
# ==============================================================================

EVENT_PRICE_UPDATE: str = "PRICE_UPDATE"

EVENT_MARKET_OPEN: str = "MARKET_OPEN"

EVENT_MARKET_CLOSE: str = "MARKET_CLOSE"

# ==============================================================================
# Redis Key Prefixes
# ==============================================================================

MARKET_KEY_PREFIX: str = "market"

# Example:
#
# market:NIFTY
# market:RELIANCE
#
# Final Redis Key:
#
# f"{MARKET_KEY_PREFIX}:{symbol}"

# ==============================================================================
# Redis Hash Fields
# ==============================================================================

FIELD_SYMBOL: str = "symbol"

FIELD_PRICE: str = "price"

FIELD_OPEN: str = "open"

FIELD_HIGH: str = "high"

FIELD_LOW: str = "low"

FIELD_VOLUME: str = "volume"

FIELD_TIMESTAMP: str = "timestamp"

# ==============================================================================
# JSON Message Fields
# ==============================================================================

MESSAGE_EVENT: str = "event"

MESSAGE_DATA: str = "data"

# ==============================================================================
# Number Formatting
# ==============================================================================

PRICE_PRECISION: int = 2

# ==============================================================================
# Market Simulation
# ==============================================================================

DEFAULT_VOLUME: int = 1000

MIN_PRICE: float = 1.0

# ==============================================================================
# Console Output
# ==============================================================================

SEPARATOR: str = "=" * 80

SHORT_SEPARATOR: str = "-" * 80

# ==============================================================================
# Logging Messages
# ==============================================================================

REDIS_CONNECTED_MESSAGE: str = "Successfully connected to Redis."

REDIS_CONNECTION_FAILED_MESSAGE: str = "Unable to connect to Redis."

PUBLISHER_STARTED_MESSAGE: str = "Market Data Publisher started."

SUBSCRIBER_STARTED_MESSAGE: str = "Subscriber started."

SIMULATOR_STARTED_MESSAGE: str = "Exchange Simulator started."

# ==============================================================================
# Time Formats
# ==============================================================================

DEFAULT_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

# ==============================================================================
# Consumer Names
# ==============================================================================

DASHBOARD: str = "Dashboard"

STRATEGY_ENGINE: str = "Strategy Engine"

ANALYTICS_ENGINE: str = "Analytics Engine"

ALERT_ENGINE: str = "Alert Engine"
