"""
===============================================================================
File: exchange_simulator.py

Purpose:
    Simulates a stock exchange by generating realistic market updates.

Business Problem:
    We don't have access to a live exchange feed.

    Instead of depending on external APIs,
    this simulator continuously generates market ticks for a list of
    symbols stored in symbols.csv.

Responsibilities:
    - Load symbols
    - Generate realistic market prices
    - Maintain High / Low / Volume
    - Produce MarketTick objects

===============================================================================
"""

from __future__ import annotations

import csv
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator

from config import settings
from models.market_tick import MarketTick


class ExchangeSimulator:
    """
    Simulates a market data feed.
    """

    def __init__(self, csv_file: Path):

        self.csv_file = csv_file

        self.market_state: Dict[str, dict] = {}

        self._load_symbols()

    # ------------------------------------------------------------------

    def _load_symbols(self) -> None:
        """
        Load all trading symbols.
        """

        with open(self.csv_file, newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                symbol = row["symbol"].upper()

                start_price = float(row["start_price"])

                self.market_state[symbol] = {

                    "price": start_price,

                    "open": start_price,

                    "high": start_price,

                    "low": start_price,

                    "volume": 1000,

                }

    # ------------------------------------------------------------------

    def _generate_next_price(
        self,
        current_price: float,
    ) -> float:
        """
        Generate next market price.

        Small movements imitate real market behaviour.
        """

        movement = random.uniform(
            -settings.MAX_PRICE_CHANGE,
            settings.MAX_PRICE_CHANGE,
        )

        return round(
            max(1.0, current_price + movement),
            2,
        )

    # ------------------------------------------------------------------

    def stream(self) -> Generator[MarketTick, None, None]:
        """
        Infinite generator of market ticks.
        """

        while True:

            for symbol, state in self.market_state.items():

                new_price = self._generate_next_price(
                    state["price"]
                )

                state["price"] = new_price

                state["high"] = max(
                    state["high"],
                    new_price,
                )

                state["low"] = min(
                    state["low"],
                    new_price,
                )

                state["volume"] += random.randint(
                    10,
                    1000,
                )

                yield MarketTick(

                    symbol=symbol,

                    price=new_price,

                    open_price=state["open"],

                    high=state["high"],

                    low=state["low"],

                    volume=state["volume"],

                    timestamp=datetime.utcnow().isoformat(),

                )

            time.sleep(
                settings.UPDATE_INTERVAL_SECONDS
            )


# ==============================================================================
# Standalone Demo
# ==============================================================================

if __name__ == "__main__":

    simulator = ExchangeSimulator(
        settings.SYMBOLS_FILE
    )

    print("=" * 80)
    print("Exchange Simulator")
    print("=" * 80)

    for index, tick in enumerate(simulator.stream()):

        print(tick)

        if index >= 20:
            break
