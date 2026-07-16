"""
===============================================================================
File: dashboard.py

Purpose
-------
Simple terminal dashboard that demonstrates how Redis Pub/Sub and
Redis Hashes work together.

Workflow
--------
Redis Pub/Sub
        │
        ▼
Receive notification
        │
        ▼
Read latest snapshot from Redis Hash
        │
        ▼
Refresh terminal

Repository
----------
low-latency-market-data-engine-using-redis-python
===============================================================================
"""

from __future__ import annotations

import os
from datetime import datetime

from infrastructure.subscriber import BaseMarketSubscriber
from models.market_tick import MarketTick


class Dashboard(BaseMarketSubscriber):
    """
    Live market dashboard.
    """

    def __init__(self):

        super().__init__()

        self.market = {}

    # -------------------------------------------------------------------------

    def process_tick(
        self,
        tick: MarketTick,
    ) -> None:

        latest = self.cache.get_tick(
            tick.symbol
        )

        if latest is None:
            return

        self.market[tick.symbol] = latest

        self.render()

    # -------------------------------------------------------------------------

    def render(self):

        os.system("clear")

        print("=" * 70)

        print("                 LIVE MARKET DASHBOARD")

        print("=" * 70)

        print()

        print(
            f"Updated : {datetime.utcnow().strftime('%H:%M:%S UTC')}"
        )

        print()

        print(
            "-" * 70
        )

        print(
            f"{'Symbol':<15}"
            f"{'Price':>12}"
            f"{'High':>12}"
            f"{'Low':>12}"
            f"{'Volume':>15}"
        )

        print(
            "-" * 70
        )

        for symbol in sorted(self.market):

            tick = self.market[symbol]

            print(

                f"{tick.symbol:<15}"

                f"{tick.price:>12.2f}"

                f"{tick.high:>12.2f}"

                f"{tick.low:>12.2f}"

                f"{tick.volume:>15,}"

            )

        print("-" * 70)

        print(
            f"Cached Symbols : {len(self.market)}"
        )


if __name__ == "__main__":

    Dashboard().start()