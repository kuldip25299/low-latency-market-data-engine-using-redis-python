"""
===============================================================================
File: main.py

Low-Latency Market Data Engine using Redis

Purpose
-------
Entry point for the demonstration project.

This launcher allows users to start individual components
without remembering Python module paths.

Repository
----------
low-latency-market-data-engine-using-redis-python
===============================================================================
"""

from __future__ import annotations

import logging
import sys

from config import settings
from consumer.dashboard import Dashboard
from producer.market_publisher import MarketPublisher


logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)


def print_banner() -> None:
    """
    Display project banner.
    """

    print("\n" + "=" * 70)
    print(" Low-Latency Market Data Engine using Redis")
    print("=" * 70)
    print("A practical demonstration of Redis Pub/Sub and Redis Hashes")
    print("=" * 70)


def print_menu() -> None:
    """
    Display available options.
    """

    print("\nChoose an option:\n")

    print("1. Start Market Publisher")
    print("2. Start Live Dashboard")
    print("3. Exit")


def start_market_publisher() -> None:
    """
    Start the market publisher.
    """

    print("\nStarting Market Publisher...\n")

    publisher = MarketPublisher()

    publisher.start()


def start_dashboard() -> None:
    """
    Start the dashboard.
    """

    print("\nStarting Live Dashboard...\n")

    dashboard = Dashboard()

    dashboard.start()


def main() -> None:
    """
    Application entry point.
    """

    while True:

        print_banner()

        print_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            start_market_publisher()

        elif choice == "2":

            start_dashboard()

        elif choice == "3":

            print("\nThank you for exploring Redis!")

            sys.exit(0)

        else:

            print("\nInvalid choice. Please try again.\n")


if __name__ == "__main__":

    main()