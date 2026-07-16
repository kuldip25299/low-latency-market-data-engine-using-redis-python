"""
===============================================================================
File: publisher.py

Purpose
-------
Publishes market events using Redis Pub/Sub.

Business Problem
----------------
Multiple applications need market updates immediately.

Instead of polling Redis repeatedly, every update is broadcast
to all subscribers.

Responsibilities
----------------
✓ Serialize MarketTick

✓ Publish to Redis Pub/Sub

✓ Return subscriber count

Repository
----------
low-latency-market-data-engine-using-redis-python
===============================================================================
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict

from infrastructure.redis_client import RedisManager
from models.market_tick import MarketTick
from config import settings

logger = logging.getLogger(__name__)


class MarketEventPublisher:
    """
    Publishes market updates to Redis Pub/Sub.
    """

    def __init__(self) -> None:

        self.client = RedisManager.get_client()

    # -------------------------------------------------------------------------

    def publish_tick(self, tick: MarketTick) -> int:

        message = json.dumps(asdict(tick))

        print(f"Publishing to channel: {settings.MARKET_DATA_CHANNEL}")
        print(message)

        subscribers = self.client.publish(
            settings.MARKET_DATA_CHANNEL,
            message,
        )

        print(f"Subscribers notified: {subscribers}")

        return subscribers