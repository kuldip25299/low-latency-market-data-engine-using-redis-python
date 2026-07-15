"""
===============================================================================
File: publisher.py

Purpose:
    Publishes real-time market events to Redis Pub/Sub.

Business Problem:
    Multiple independent services need to receive market updates
    immediately after they arrive.

    Rather than allowing every consumer to poll Redis repeatedly,
    the Publisher broadcasts market events to a Redis channel.

Responsibilities:
    - Serialize market events
    - Publish events to Redis
    - Hide Redis Pub/Sub implementation details

Author:
    Kuldip Awachar
===============================================================================
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict

from config import settings
from models.market_tick import MarketTick
from redis.redis_client import RedisManager

logger = logging.getLogger(__name__)


class MarketEventPublisher:
    """
    Publishes market events using Redis Pub/Sub.
    """

    def __init__(self) -> None:
        self.client = RedisManager.get_client()

    def publish(self, tick: MarketTick) -> int:
        """
        Publish a market update.

        Parameters
        ----------
        tick : MarketTick

        Returns
        -------
        int
            Number of subscribers that received the message.
        """

        message = json.dumps(asdict(tick))

        subscribers = self.client.publish(
            settings.MARKET_DATA_CHANNEL,
            message,
        )

        logger.debug(
            "Published %s to %s (%s subscribers)",
            tick.symbol,
            settings.MARKET_DATA_CHANNEL,
            subscribers,
        )

        return subscribers
