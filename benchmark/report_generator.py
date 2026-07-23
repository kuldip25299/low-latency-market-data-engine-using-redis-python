"""
benchmark/report_generator.py

Generates benchmark reports in multiple formats.

Supported Formats
-----------------
1. JSON
2. CSV
3. TXT (Human Readable)

Author:
    Kuldip Awachar

Repository:
    low-latency-market-data-engine-using-redis-python
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Any

from benchmark.common import current_timestamp


class ReportGenerator:
    """
    Generate benchmark reports.

    Directory Structure

    benchmark/
        reports/
            benchmark_2026-07-16_12-30-15/
                report.json
                report.csv
                report.txt
    """

    def __init__(self):

        timestamp = current_timestamp()

        self.output_directory = (
            Path(__file__).parent
            / "reports"
            / f"benchmark_{timestamp}"
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -----------------------------------------------------

    def save_json(self, results: Dict[str, Any]) -> Path:
        """
        Save benchmark results as JSON.
        """

        file_path = self.output_directory / "report.json"

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(
                results,
                file,
                indent=4,
                default=str,
            )

        return file_path

    # -----------------------------------------------------

    def save_csv(self, results: Dict[str, Any]) -> Path:
        """
        Save benchmark results as CSV.

        Nested dictionaries are flattened.
        """

        file_path = self.output_directory / "report.csv"

        rows = []

        def flatten(prefix, value):

            if isinstance(value, dict):

                for k, v in value.items():
                    flatten(f"{prefix}.{k}" if prefix else k, v)

            else:

                rows.append([prefix, value])

        flatten("", results)

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow(["Metric", "Value"])

            writer.writerows(rows)

        return file_path

    # -----------------------------------------------------

    def save_text(self, results: Dict[str, Any]) -> Path:
        """
        Save benchmark as formatted TXT report.
        """

        file_path = self.output_directory / "report.txt"

        with open(file_path, "w", encoding="utf-8") as file:

            file.write("=" * 70)
            file.write("\n")

            file.write("REDIS BENCHMARK REPORT".center(70))

            file.write("\n")

            file.write("=" * 70)

            file.write("\n\n")

            self._write_dictionary(
                file=file,
                dictionary=results,
            )

        return file_path

    # -----------------------------------------------------

    def _write_dictionary(
        self,
        file,
        dictionary,
        indent=0,
    ):
        """
        Recursive dictionary writer.
        """

        spacing = " " * indent

        for key, value in dictionary.items():

            if isinstance(value, dict):

                file.write(f"{spacing}{key}\n")

                self._write_dictionary(
                    file,
                    value,
                    indent + 4,
                )

            else:

                file.write(
                    f"{spacing}{key:<30}: {value}\n"
                )

    # -----------------------------------------------------

    def generate(self, results: Dict[str, Any]):
        """
        Generate all reports.
        """

        json_file = self.save_json(results)

        csv_file = self.save_csv(results)

        txt_file = self.save_text(results)

        print()

        print("=" * 70)

        print("REPORTS GENERATED".center(70))

        print("=" * 70)

        print(f"JSON : {json_file}")

        print(f"CSV  : {csv_file}")

        print(f"TXT  : {txt_file}")

        print("=" * 70)


# ------------------------------------------------------------------

if __name__ == "__main__":

    sample_report = {

        "benchmark": "Redis Pub/Sub",

        "messages": 100000,

        "latency": {

            "average_ms": 2.31,

            "median_ms": 2.20,

            "minimum_ms": 1.85,

            "maximum_ms": 5.60,

            "p95_ms": 3.41,

            "p99_ms": 4.12,
        },

        "throughput": {

            "ticks_per_second": 152340,
        },

        "system": {

            "cpu_percent": 8.3,

            "memory_mb": 17.4,
        },
    }

    generator = ReportGenerator()

    generator.generate(sample_report)