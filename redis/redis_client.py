"""
===============================================================================
File: redis_client.py

Purpose:
    Creates and manages a reusable Redis connection for the application.

Business Problem:
    Every producer and consumer needs to communicate with Redis.
    Creating a new Redis connection for every request increases
    latency, wastes TCP connections, and duplicates code.

    This module provides a single shared Redis client backed by a
    connection pool that can be reused across the entire application.

Responsibilities:
    - Create Redis connection pool
    - Validate Redis connectivity
    - Return shared Redis client
    - Handle connection failures gracefully
    - Provide a clean API for the rest of the project

Author:
    Kuldip Awachar

Repository:
    low-latency-market-data-engine-using-redis-python
===============================================================================
"""

from __future__ import annotations

import logging
from typing import Optional

import redis
from redis import Redis
from redis.connection import ConnectionPool
from redis.exceptions import ConnectionError, RedisError, TimeoutError

from config import settings
from config.constants import (
    REDIS_CONNECTED_MESSAGE,
    REDIS_CONNECTION_FAILED_MESSAGE,
)

# ------------------------------------------------------------------------------
# Configure logging
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)

logger = logging.getLogger(__name__)


class RedisManager:
    """
    Singleton-style Redis connection manager.

    This class owns the Redis connection pool and exposes a shared
    Redis client to the rest of the application.

    Example:
        client = RedisManager.get_client()

        client.set("hello", "world")
    """

    _pool: Optional[ConnectionPool] = None
    _client: Optional[Redis] = None

    @classmethod
    def _create_connection_pool(cls) -> ConnectionPool:
        """
        Create a Redis connection pool.

        Returns
        -------
        ConnectionPool
            Configured Redis connection pool.
        """

        logger.info("Creating Redis connection pool...")

        return ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            max_connections=50,
            socket_timeout=5,
            socket_connect_timeout=5,
            health_check_interval=30,
        )

    @classmethod
    def get_client(cls) -> Redis:
        """
        Returns a shared Redis client.

        If no client exists, one is created using a connection pool.

        Returns
        -------
        redis.Redis

        Raises
        ------
        redis.exceptions.ConnectionError
            If Redis is unavailable.
        """

        if cls._client is None:

            if cls._pool is None:
                cls._pool = cls._create_connection_pool()

            cls._client = Redis(connection_pool=cls._pool)

            cls._verify_connection()

        return cls._client

    @classmethod
    def _verify_connection(cls) -> None:
        """
        Verify Redis connectivity using PING.

        Raises
        ------
        ConnectionError
            If Redis cannot be reached.
        """

        try:
            assert cls._client is not None

            cls._client.ping()

            logger.info(REDIS_CONNECTED_MESSAGE)

        except (ConnectionError, TimeoutError) as exc:

            logger.error(REDIS_CONNECTION_FAILED_MESSAGE)

            raise ConnectionError(
                "Unable to establish connection with Redis."
            ) from exc

    @classmethod
    def close(cls) -> None:
        """
        Disconnect all pooled Redis connections.

        Normally not required because Python closes sockets when the
        application exits, but explicitly closing connections is useful
        during testing or graceful shutdown.
        """

        if cls._pool is not None:

            logger.info("Closing Redis connection pool...")

            cls._pool.disconnect()

            cls._pool = None
            cls._client = None

            logger.info("Redis connection pool closed.")


# ------------------------------------------------------------------------------
# Standalone execution
# ------------------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 80)
    print("Redis Connection Test")
    print("=" * 80)

    try:

        client = RedisManager.get_client()

        client.set("redis:test", "Connection Successful")

        value = client.get("redis:test")

        print(f"Stored Value : {value}")

        print("\nRedis connection is working correctly.")

    except RedisError as exc:

        logger.exception("Redis connection test failed.")

        print(f"\nError: {exc}")

    finally:

        RedisManager.close()
