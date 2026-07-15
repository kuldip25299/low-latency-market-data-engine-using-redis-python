"""
===============================================================================
Market Publisher

Coordinates the complete market data pipeline.

Exchange Simulator
        │
        ▼
Latest Price Cache
        │
        ▼
Redis Pub/Sub
===============================================================================
"""

from producer.exchange_simulator import ExchangeSimulator

from redis.latest_price_cache import LatestPriceCache

from redis.publisher import MarketEventPublisher

from config import settings


class MarketPublisher:
    """
    Coordinates the market data pipeline.
    """

    def __init__(self):

        self.simulator = ExchangeSimulator(
            settings.SYMBOLS_FILE
        )

        self.cache = LatestPriceCache()

        self.publisher = MarketEventPublisher()

    def start(self):

        for tick in self.simulator.stream():

            # Store latest state
            self.cache.update_market_data(
                symbol=tick.symbol,
                price=tick.price,
                open_price=tick.open_price,
                high=tick.high,
                low=tick.low,
                volume=tick.volume,
            )

            # Broadcast update
            self.publisher.publish(tick)


if __name__ == "__main__":

    MarketPublisher().start()
