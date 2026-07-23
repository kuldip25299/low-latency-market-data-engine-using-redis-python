"""
benchmark/charts.py

Generate benchmark charts automatically.

This module creates publication-quality PNG charts that can be
used directly in:

- README.md
- GitHub documentation
- LinkedIn posts
- Technical blogs
- Benchmark reports

Author:
    Kuldip Awachar

Repository:
    low-latency-market-data-engine-using-redis-python
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt


class ChartGenerator:
    """
    Generate benchmark charts.

    Charts are stored under:

    benchmark/
        reports/
            benchmark_xxx/
                graphs/
                    latency.png
                    throughput.png
                    cpu_usage.png
                    memory_usage.png
    """

    def __init__(self, output_directory: Path):

        self.graph_directory = output_directory / "graphs"

        self.graph_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------

    def latency_comparison(
        self,
        traditional_latency: float,
        redis_latency: float,
    ):
        """
        Create latency comparison chart.
        """

        labels = [
            "Traditional",
            "Redis",
        ]

        values = [
            traditional_latency,
            redis_latency,
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(labels, values)

        plt.title("Average Latency Comparison")

        plt.ylabel("Milliseconds")

        plt.tight_layout()

        output = self.graph_directory / "latency_comparison.png"

        plt.savefig(output, dpi=300)

        plt.close()

        print(f"Generated: {output}")

    # ---------------------------------------------------------

    def throughput_comparison(
        self,
        traditional_tps: float,
        redis_tps: float,
    ):
        """
        Compare throughput.
        """

        labels = [
            "Traditional",
            "Redis",
        ]

        values = [
            traditional_tps,
            redis_tps,
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(labels, values)

        plt.title("Throughput Comparison")

        plt.ylabel("Ticks / Second")

        plt.tight_layout()

        output = self.graph_directory / "throughput_comparison.png"

        plt.savefig(output, dpi=300)

        plt.close()

        print(f"Generated: {output}")

    # ---------------------------------------------------------

    def cpu_usage(
        self,
        traditional_cpu: float,
        redis_cpu: float,
    ):
        """
        CPU comparison.
        """

        labels = [
            "Traditional",
            "Redis",
        ]

        values = [
            traditional_cpu,
            redis_cpu,
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(labels, values)

        plt.title("CPU Usage")

        plt.ylabel("CPU %")

        plt.tight_layout()

        output = self.graph_directory / "cpu_usage.png"

        plt.savefig(output, dpi=300)

        plt.close()

        print(f"Generated: {output}")

    # ---------------------------------------------------------

    def memory_usage(
        self,
        traditional_memory: float,
        redis_memory: float,
    ):
        """
        Memory comparison.
        """

        labels = [
            "Traditional",
            "Redis",
        ]

        values = [
            traditional_memory,
            redis_memory,
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(labels, values)

        plt.title("Memory Usage")

        plt.ylabel("Memory (MB)")

        plt.tight_layout()

        output = self.graph_directory / "memory_usage.png"

        plt.savefig(output, dpi=300)

        plt.close()

        print(f"Generated: {output}")

    # ---------------------------------------------------------

    def benchmark_summary(
        self,
        benchmark_results: Dict[str, float],
    ):
        """
        Create one chart containing all benchmark metrics.

        Example input:

        {
            "Latency(ms)":2.5,
            "CPU(%)":8,
            "Memory(MB)":14,
            "Throughput(K/s)":150
        }
        """

        labels = list(benchmark_results.keys())

        values = list(benchmark_results.values())

        plt.figure(figsize=(10, 5))

        plt.bar(labels, values)

        plt.title("Benchmark Summary")

        plt.tight_layout()

        output = self.graph_directory / "benchmark_summary.png"

        plt.savefig(output, dpi=300)

        plt.close()

        print(f"Generated: {output}")


# ----------------------------------------------------------------------

if __name__ == "__main__":

    report_directory = (
        Path(__file__).parent
        / "reports"
        / "sample_report"
    )

    report_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    charts = ChartGenerator(report_directory)

    charts.latency_comparison(
        traditional_latency=520,
        redis_latency=2.8,
    )

    charts.throughput_comparison(
        traditional_tps=1200,
        redis_tps=154000,
    )

    charts.cpu_usage(
        traditional_cpu=31,
        redis_cpu=8,
    )

    charts.memory_usage(
        traditional_memory=26,
        redis_memory=12,
    )

    charts.benchmark_summary(
        {
            "Latency(ms)": 2.8,
            "CPU(%)": 8,
            "Memory(MB)": 12,
            "TPS(K)": 154,
        }
    )

    print()

    print("All benchmark charts generated successfully.")