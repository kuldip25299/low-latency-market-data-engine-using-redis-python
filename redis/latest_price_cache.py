"""
===============================================================================
File: latest_price_cache.py

Purpose:
    Provides a clean abstraction for storing and retrieving the latest
    market prices from Redis.

Business Problem:
    Multiple services (Dashboard, Strategy Engine, Analytics Engine,
    Alert Engine) need access to the latest market state.

    Instead of allowing every module to execute raw Redis commands,
    this class centralizes all Redis cache operations.

Benefits:
    - Hides Redis implementation details
    - Prevents duplicate Redis code
    - Makes future changes easier
    - Improves maintainability
    - Follows the Repository Pattern

Author:
    Kuldip Awachar

Repository:
    low-latency-market-data-engine-using-redis-python
===============================================================================
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, List, Optional

from config.constants import (
    FIELD_HIGH,
    FIELD_LOW,
    FIELD_OPEN,
    FIELD_PRICE,
    FIELD_SYMBOL,
    FIELD_TIMESTAMP,
    FIELD_VOLUME,
    MARKET_KEY_PREFIX,
)
from redis.redis_client import RedisManager

logger = logging.getLogger(__name__)


class LatestPriceCache:
    """
    Repository responsible for storing and retrieving
    the latest market state from Redis.
    """

    def __init__(self) -> None:
        self.client = RedisManager.get_client()

    @staticmethod
    def _build_key(symbol: str) -> str:
        """
        Build Redis key for a market symbol.

        Example:
            market:NIFTY
            market:TCS
        """
        return f"{MARKET_KEY_PREFIX}:{symbol.upper()}"

    def update_market_data(
        self,
        symbol: str,
        price: float,
        open_price: float,
        high: float,
        low: float,
        volume: int,
    ) -> None:
        """
        Store the latest market snapshot for a symbol.

        Parameters
        ----------
        symbol : str
        price : float
        open_price : float
        high : float
        low : float
        volume : int
        """

        key = self._build_key(symbol)

        market_snapshot = {
            FIELD_SYMBOL: symbol.upper(),
            FIELD_PRICE: price,
            FIELD_OPEN: open_price,
            FIELD_HIGH: high,
            FIELD_LOW: low,
            FIELD_VOLUME: volume,
            FIELD_TIMESTAMP: datetime.utcnow().isoformat(),
        }

        self.client.hset(
            key,
            mapping=market_snapshot,
        )

        logger.debug("Updated Redis cache for %s", symbol)

    def get_market_data(
        self,
        symbol: str,
    ) -> Optional[Dict[str, str]]:
        """
        Retrieve latest market snapshot.

        Returns
        -------
        dict | None
        """

        key = self._build_key(symbol)

        result = self.client.hgetall(key)

        if not result:
            return None

        return result

    def delete_symbol(
        self,
        symbol: str,
    ) -> bool:
        """
        Remove symbol from cache.

        Returns
        -------
        bool
            True if deleted.
        """

        key = self._build_key(symbol)

        deleted = self.client.delete(key)

        return bool(deleted)

    def symbol_exists(
        self,
        symbol: str,
    ) -> bool:
        """
        Check whether symbol exists.
        """

        return self.client.exists(self._build_key(symbol)) == 1

    def get_all_symbols(self) -> List[str]:
        """
        Return all cached market symbols.

        Example

            market:NIFTY
            market:TCS
            market:INFY

        becomes

            NIFTY
            TCS
            INFY
        """

        keys = self.client.keys(f"{MARKET_KEY_PREFIX}:*")

        symbols = [
            key.split(":")[1]
            for key in keys
        ]

        symbols.sort()

        return symbols

    def clear_cache(self) -> int:
        """
        Remove every cached market symbol.

        Returns
        -------
        int
            Number of deleted symbols.
        """

        keys = self.client.keys(f"{MARKET_KEY_PREFIX}:*")

        if not keys:
            return 0

        return self.client.delete(*keys)


# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    cache = LatestPriceCache()

    print("=" * 80)
    print("Latest Price Cache Demo")
    print("=" * 80)

    cache.clear_cache()

    cache.update_market_data(
        symbol="NIFTY",
        price=25540,
        open_price=25500,
        high=25560,
        low=25490,
        volume=120000,
    )

    print("\nStored Snapshot\n")

    print(cache.get_market_data("NIFTY"))

    print("\nCached Symbols\n")

    print(cache.get_all_symbols())

    print("\nDeleting Symbol...\n")

    cache.delete_symbol("NIFTY")

    print(cache.get_market_data("NIFTY"))
