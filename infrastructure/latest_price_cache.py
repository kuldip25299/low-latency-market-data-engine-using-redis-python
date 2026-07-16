"""
===============================================================================
File: latest_price_cache.py

Purpose
-------
Provides a clean abstraction for storing and retrieving the latest market
snapshot from Redis.

Business Problem
----------------
Multiple applications need the latest market price:

    • Dashboard
    • Strategy Engine
    • Analytics Engine
    • Alert Engine

Instead of allowing every component to execute raw Redis commands,
this class centralizes all cache operations.

Benefits
--------
✓ Single place for Redis Hash operations

✓ Hides Redis implementation details

✓ Works directly with MarketTick objects

✓ Easy to replace Redis in future if needed

Repository
----------
low-latency-market-data-engine-using-redis-python
===============================================================================
"""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import List, Optional

from infrastructure.redis_client import RedisManager
from models.market_tick import MarketTick
from config.constants import MARKET_KEY_PREFIX

logger = logging.getLogger(__name__)


class LatestPriceCache:
    """
    Repository responsible for storing and retrieving
    the latest market snapshot.
    """

    def __init__(self) -> None:
        self.client = RedisManager.get_client()

    # -------------------------------------------------------------------------
    # Private Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _build_key(symbol: str) -> str:
        """
        Build Redis key.

        Example
        -------
        market:NIFTY

        market:TCS

        market:INFY
        """

        return f"{MARKET_KEY_PREFIX}:{symbol.upper()}"

    # -------------------------------------------------------------------------
    # Public Methods
    # -------------------------------------------------------------------------

    def update_tick(self, tick: MarketTick) -> None:
        """
        Store the latest market snapshot.

        Parameters
        ----------
        tick : MarketTick
        """

        key = self._build_key(tick.symbol)

        mapping = asdict(tick)

        # Keep Redis field names short and finance friendly.
        mapping["open"] = mapping.pop("open_price")

        self.client.hset(
            key,
            mapping=mapping,
        )

        logger.debug(
            "Updated latest price cache for %s",
            tick.symbol,
        )

    # -------------------------------------------------------------------------

    def get_tick(
        self,
        symbol: str,
    ) -> Optional[MarketTick]:
        """
        Retrieve latest market snapshot.

        Returns
        -------
        MarketTick | None
        """

        data = self.client.hgetall(
            self._build_key(symbol)
        )

        if not data:
            return None

        return MarketTick(
            symbol=data["symbol"],
            price=float(data["price"]),
            open_price=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            volume=int(data["volume"]),
            timestamp=data["timestamp"],
        )

    # -------------------------------------------------------------------------

    def symbol_exists(
        self,
        symbol: str,
    ) -> bool:
        """
        Check whether symbol exists in Redis.
        """

        return bool(
            self.client.exists(
                self._build_key(symbol)
            )
        )

    # -------------------------------------------------------------------------

    def delete_tick(
        self,
        symbol: str,
    ) -> bool:
        """
        Remove symbol from cache.

        Returns
        -------
        bool
        """

        deleted = self.client.delete(
            self._build_key(symbol)
        )

        return bool(deleted)

    # -------------------------------------------------------------------------

    def get_all_symbols(self) -> List[str]:
        """
        Returns every cached market symbol.

        Example
        -------

        market:NIFTY
        market:TCS
        market:INFY

        becomes

        NIFTY
        TCS
        INFY
        """

        keys = self.client.keys(
            f"{MARKET_KEY_PREFIX}:*"
        )

        symbols = [
            key.replace(
                f"{MARKET_KEY_PREFIX}:",
                "",
            )
            for key in keys
        ]

        symbols.sort()

        return symbols

    # -------------------------------------------------------------------------

    def clear(self) -> int:
        """
        Remove every market symbol.

        Useful during benchmarking.

        Returns
        -------
        int
            Number of deleted keys.
        """

        keys = self.client.keys(
            f"{MARKET_KEY_PREFIX}:*"
        )

        if not keys:
            return 0

        return self.client.delete(*keys)


# =============================================================================
# Standalone Demo
# =============================================================================

if __name__ == "__main__":

    from datetime import datetime

    cache = LatestPriceCache()

    cache.clear()

    tick = MarketTick(
        symbol="NIFTY",
        price=25542.25,
        open_price=25510.00,
        high=25560.00,
        low=25495.00,
        volume=245000,
        timestamp=datetime.utcnow().isoformat(),
    )

    print("=" * 80)
    print("Saving Tick...")
    print("=" * 80)

    cache.update_tick(tick)

    print("\nReading Tick...\n")

    latest = cache.get_tick("NIFTY")

    print(latest)

    print("\nCached Symbols\n")

    print(cache.get_all_symbols())

    print("\nDeleting Tick...\n")

    # cache.delete_tick("NIFTY")

    # print(cache.get_tick("NIFTY"))