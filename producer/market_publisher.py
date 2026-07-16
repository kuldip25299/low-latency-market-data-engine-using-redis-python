"""
===============================================================================
File: market_publisher.py

Purpose
-------
Coordinates the complete market data pipeline.

Architecture
------------
Exchange Simulator
        │
        ▼
MarketTick
        │
        ▼
LatestPriceCache (Redis Hash)
        │
        ▼
Redis Pub/Sub
        │
        ▼
Consumers

Business Problem
----------------
An exchange continuously produces market updates.

Those updates need to:

1. Store the latest market state.
2. Broadcast the update to every interested application.

This class coordinates those steps.

Repository
----------
low-latency-market-data-engine-using-redis-python
===============================================================================
"""

from __future__ import annotations

import logging

from infrastructure.latest_price_cache import LatestPriceCache
from infrastructure.publisher import MarketEventPublisher
from producer.exchange_simulator import ExchangeSimulator
from config import settings

logger = logging.getLogger(__name__)


class MarketPublisher:
    """
    Coordinates the market data pipeline.
    """

    def __init__(self) -> None:

        self.simulator = ExchangeSimulator(
            settings.SYMBOLS_FILE
        )

        self.cache = LatestPriceCache()

        self.publisher = MarketEventPublisher()

    # -------------------------------------------------------------------------

    def start(self) -> None:
        """
        Start publishing market data.
        """

        print("Starting simulator...")

        for tick in self.simulator.stream():

            print("Tick received:", tick)

            self.cache.update_tick(tick)

            subscribers = self.publisher.publish_tick(tick)

            print("Published to", subscribers, "subscriber(s)")


# =============================================================================
# Standalone Execution
# =============================================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format="%(asctime)s | %(levelname)-8s | %(message)s",
    )

    MarketPublisher().start()