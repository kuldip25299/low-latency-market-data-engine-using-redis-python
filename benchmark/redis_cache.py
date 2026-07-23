"""
benchmark/redis_cache.py

Simple Redis Cache Helper used for benchmarking.

Business Problem
----------------
Applications often need to display the latest market price.

Without Redis:
    Dashboard
        ↓
    Database
        ↓
    SELECT latest price

With Redis:
    Dashboard
        ↓
    Redis Hash
        ↓
    HGETALL market:NIFTY

Redis keeps the latest market data in memory,
making reads significantly faster than querying
the database repeatedly.

Author:
    Kuldip Awachar
"""

from __future__ import annotations

import json

from infrastructure.redis_client import RedisManager


class RedisCache:
    """
    Simple Redis cache helper.

    Stores each symbol as a Redis Hash.

    Example

        market:NIFTY
        market:TCS
        market:INFY
    """

    def __init__(self):

        self.redis = RedisManager.get_client()

    # ---------------------------------------------------------

    def save_price(
        self,
        symbol,
        price,
        open_price,
        high,
        low,
        volume,
        updated_at,
    ):
        """
        Store latest market price.

        Redis Key

            market:NIFTY
        """

        key = f"market:{symbol}"

        self.redis.hset(
            key,
            mapping={
                "symbol": symbol,
                "price": price,
                "open_price": open_price,
                "high": high,
                "low": low,
                "volume": volume,
                "updated_at": updated_at,
            },
        )

    # ---------------------------------------------------------

    def get_latest_price(self, symbol):
        """
        Read latest market price.
        """

        key = f"market:{symbol}"

        data = self.redis.hgetall(key)

        if not data:
            return None

        return data

    # ---------------------------------------------------------

    def total_keys(self):
        """
        Number of cached market symbols.
        """

        return len(self.redis.keys("market:*"))

    # ---------------------------------------------------------

    def delete_all(self):
        """
        Remove all benchmark cache.

        Safe to call before each benchmark.
        """

        keys = self.redis.keys("market:*")

        if keys:

            self.redis.delete(*keys)

    # ---------------------------------------------------------

    def seed_sample_data(self):
        """
        Populate Redis with sample data.
        """

        self.delete_all()

        sample_data = [

            ("NIFTY",25542.50,25510.00,25560.00,25495.00,245000,"2026-07-16 10:30:00"),

            ("BANKNIFTY",57120.75,57080.00,57190.00,56990.00,182000,"2026-07-16 10:30:00"),

            ("RELIANCE",2965.40,2980.00,2995.00,2955.00,101500,"2026-07-16 10:30:00"),

            ("TCS",3892.20,3920.00,3944.00,3885.00,84200,"2026-07-16 10:30:00"),

            ("INFY",1730.60,1685.00,1740.00,1678.00,54600,"2026-07-16 10:30:00"),
        ]

        for row in sample_data:

            self.save_price(*row)

    # ---------------------------------------------------------

    def print_cache(self):
        """
        Print all cached data.

        Useful for learning.
        """

        print()

        print("=" * 60)

        print("REDIS CACHE")

        print("=" * 60)

        for key in sorted(self.redis.keys("market:*")):

            print()

            print(key)

            print(json.dumps(
                self.redis.hgetall(key),
                indent=4,
            ))

    # ---------------------------------------------------------

    def close(self):
        """
        Close Redis connection.
        """

        RedisManager.close()


# ------------------------------------------------------------------

if __name__ == "__main__":

    cache = RedisCache()

    cache.seed_sample_data()

    print()

    print("Redis Cache Populated Successfully")

    print()

    print("Total Cached Symbols")

    print(cache.total_keys())

    print()

    print("Latest NIFTY Price")

    print(cache.get_latest_price("NIFTY"))

    cache.print_cache()

    cache.close()