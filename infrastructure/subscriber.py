"""
===============================================================================
File: subscriber.py

Purpose:
    Base Redis Pub/Sub subscriber used by every consumer.

Business Problem
----------------
Every consumer (Dashboard, Strategy Engine, Analytics Engine,
Alert Engine) needs to subscribe to the same Redis channel.

Without a shared base class, every consumer would duplicate:

    • Redis connection
    • Subscription logic
    • JSON parsing
    • Error handling
    • Logging

This class centralizes that behaviour.

Responsibilities
----------------
✓ Subscribe to Redis channel

✓ Listen continuously

✓ Convert JSON into MarketTick objects

✓ Invoke child class callback

Author:
    Kuldip Awachar
===============================================================================
"""

from __future__ import annotations

import json
import logging
from abc import ABC
from abc import abstractmethod

from models.market_tick import MarketTick

from infrastructure.redis_client import RedisManager
from infrastructure.latest_price_cache import LatestPriceCache


from config import settings

logger = logging.getLogger(__name__)


class BaseMarketSubscriber(ABC):
    """
    Base class for all market consumers.

    Child classes only need to implement:

        process_tick()
    """

    def __init__(self):

        self.client = RedisManager.get_client()

        self.pubsub = self.client.pubsub()

        self.cache = LatestPriceCache()

    # ------------------------------------------------------------------

    def start(self):

        """
        Start listening for market updates.
        """

        logger.info(
            "%s subscribed to %s",
            self.__class__.__name__,
            settings.MARKET_DATA_CHANNEL,
        )

        self.pubsub.subscribe(
            settings.MARKET_DATA_CHANNEL
        )

        for message in self.pubsub.listen():

            if message["type"] != "message":
                continue

            tick = self._parse_message(
                message["data"]
            )

            self.process_tick(
                tick
            )

    # ------------------------------------------------------------------

    @staticmethod
    def _parse_message(
        payload: str,
    ) -> MarketTick:

        """
        Convert JSON payload into MarketTick.
        """

        data = json.loads(payload)

        return MarketTick(

            symbol=data["symbol"],

            price=float(data["price"]),

            open_price=float(data["open_price"]),

            high=float(data["high"]),

            low=float(data["low"]),

            volume=int(data["volume"]),

            timestamp=data["timestamp"],

        )

    # ------------------------------------------------------------------

    @abstractmethod
    def process_tick(
        self,
        tick: MarketTick,
    ) -> None:
        """
        Handle market update.

        Every child implements this.
        """
        pass
