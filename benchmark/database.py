"""
benchmark/database.py

This module creates a small SQLite database used for benchmarking.

Business Problem
----------------
Imagine a dashboard that displays the latest stock prices.

Without Redis:
    Dashboard
        ↓
    Database
        ↓
    SELECT price ...

Every dashboard refresh queries the database.

With Redis:
    Dashboard
        ↓
      Redis
        ↓
    Instant lookup

This module represents the traditional database.

Author:
    Kuldip Awachar
"""

from pathlib import Path
import sqlite3


class BenchmarkDatabase:
    """
    SQLite database helper used only for benchmarking.
    """

    def __init__(self):

        data_directory = Path(__file__).parent / "data"
        data_directory.mkdir(exist_ok=True)

        self.database_path = data_directory / "sqlite_market.db"

        self.connection = sqlite3.connect(self.database_path)

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_table()

    # ---------------------------------------------------------

    def create_table(self):
        """
        Create market_prices table.
        """

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS market_prices (

                symbol TEXT PRIMARY KEY,

                price REAL NOT NULL,

                open_price REAL,

                high REAL,

                low REAL,

                volume INTEGER,

                updated_at TEXT
            )
            """
        )

        self.connection.commit()

    # ---------------------------------------------------------

    def insert_or_update(
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
        Insert or update latest price.
        """

        self.cursor.execute(
            """
            INSERT INTO market_prices
            VALUES (?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(symbol)

            DO UPDATE SET

                price=excluded.price,

                open_price=excluded.open_price,

                high=excluded.high,

                low=excluded.low,

                volume=excluded.volume,

                updated_at=excluded.updated_at
            """,
            (
                symbol,
                price,
                open_price,
                high,
                low,
                volume,
                updated_at,
            ),
        )

        self.connection.commit()

    # ---------------------------------------------------------

    def get_latest_price(self, symbol):
        """
        Read one symbol.
        """

        self.cursor.execute(
            """
            SELECT *

            FROM market_prices

            WHERE symbol = ?
            """,
            (symbol,),
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    # ---------------------------------------------------------

    def get_all_prices(self):
        """
        Return all rows.
        """

        self.cursor.execute(
            """
            SELECT *

            FROM market_prices
            """
        )

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]

    # ---------------------------------------------------------

    def total_records(self):
        """
        Number of rows.
        """

        self.cursor.execute(
            """
            SELECT COUNT(*)

            FROM market_prices
            """
        )

        return self.cursor.fetchone()[0]

    # ---------------------------------------------------------

    def seed_sample_data(self):
        """
        Populate database with sample market data.

        Safe to call multiple times.
        """

        sample_data = [

            ("NIFTY", 25542.50, 25510.00, 25560.00, 25495.00, 245000, "2026-07-16 10:30:00"),

            ("BANKNIFTY", 57120.75, 57080.00, 57190.00, 56990.00, 182000, "2026-07-16 10:30:00"),

            ("RELIANCE", 2965.40, 2980.00, 2995.00, 2955.00, 101500, "2026-07-16 10:30:00"),

            ("TCS", 3892.20, 3920.00, 3944.00, 3885.00, 84200, "2026-07-16 10:30:00"),

            ("INFY", 1730.60, 1685.00, 1740.00, 1678.00, 54600, "2026-07-16 10:30:00"),
        ]

        for row in sample_data:

            self.insert_or_update(*row)

    # ---------------------------------------------------------

    def close(self):

        self.connection.close()


# ------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("SQLite Benchmark Database")
    print("=" * 60)

    database = BenchmarkDatabase()

    database.seed_sample_data()

    print()

    print("Database File")
    print(database.database_path)

    print()

    print("Total Records")
    print(database.total_records())

    print()

    print("Sample Record")

    print(database.get_latest_price("NIFTY"))

    database.close()

    print()

    print("Done.")