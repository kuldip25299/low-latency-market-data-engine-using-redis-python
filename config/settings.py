"""
===============================================================================
File: settings.py

Purpose:
    Centralized configuration for the Low Latency Market Data Engine.

Business Problem:
    Multiple modules (Producer, Consumers, Redis, Benchmarks) require
    common configuration values such as Redis host, port, channels,
    and simulation parameters.

    Instead of hardcoding values throughout the project, we keep all
    configurable settings in one place.

Benefits:
    - Easy to modify configuration
    - Avoids duplicate values
    - Improves maintainability
    - Simplifies deployment

Author:
    Kuldip Awachar

Repository:
    low-latency-market-data-engine-using-redis-python
===============================================================================
"""

from pathlib import Path

# ==============================================================================
# Project Paths
# ==============================================================================

# Root directory of the repository
BASE_DIR = Path(__file__).resolve().parent.parent

# Symbols CSV used by the exchange simulator
SYMBOLS_FILE = BASE_DIR / "producer" / "symbols.csv"

# ==============================================================================
# Redis Configuration
# ==============================================================================

REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
REDIS_PASSWORD: str | None = None

# ==============================================================================
# Redis Channels
# ==============================================================================

# Channel used for broadcasting live market updates.
MARKET_DATA_CHANNEL: str = "market:data"

# Prefix used for storing latest market snapshots.
MARKET_CACHE_PREFIX: str = "market"

# ==============================================================================
# Exchange Simulator
# ==============================================================================

# Number of market updates generated every second.
#
# Example:
# UPDATE_INTERVAL_SECONDS = 0.01
# produces roughly 100 updates/sec.
UPDATE_INTERVAL_SECONDS: float = 0.05

# Maximum random price movement per update.
MAX_PRICE_CHANGE: float = 5.0

# Initial price assigned to newly loaded symbols.
DEFAULT_START_PRICE: float = 1000.0

# ==============================================================================
# Logging
# ==============================================================================

LOG_LEVEL: str = "INFO"

# ==============================================================================
# Benchmark Configuration
# ==============================================================================

TOTAL_BENCHMARK_UPDATES: int = 100_000

# ==============================================================================
# Consumer Configuration
# ==============================================================================

ENABLE_DASHBOARD: bool = True
ENABLE_ANALYTICS: bool = True
ENABLE_ALERT_ENGINE: bool = True
ENABLE_STRATEGY_ENGINE: bool = True
