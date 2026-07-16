"""
benchmark/common.py

Common utility functions shared by all benchmark scripts.

This module provides helper methods for:

1. High precision timing
2. Benchmark statistics
3. Pretty printing
4. Timestamp generation
5. Duration formatting

Author:
    Kuldip Awachar

Repository:
    low-latency-market-data-engine-using-redis-python
"""

from __future__ import annotations

import statistics
import time
from datetime import datetime
from typing import List, Dict


class Timer:
    """
    High precision timer.

    Uses perf_counter_ns() which provides the highest
    available timer resolution in Python.

    Example:

        timer = Timer()

        timer.start()

        # do work

        elapsed = timer.stop()

        print(elapsed)
    """

    def __init__(self):

        self._start = 0

    def start(self):

        self._start = time.perf_counter_ns()

    def stop(self) -> float:
        """
        Returns elapsed time in milliseconds.
        """

        end = time.perf_counter_ns()

        return (end - self._start) / 1_000_000


def current_timestamp() -> str:
    """
    Current timestamp used for benchmark reports.

    Example

    2026-07-16_14-42-30
    """

    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def format_duration(milliseconds: float) -> str:
    """
    Convert milliseconds into a readable string.

    Examples

    12.52 ms

    1.22 sec

    3 min 10 sec
    """

    if milliseconds < 1000:
        return f"{milliseconds:.2f} ms"

    seconds = milliseconds / 1000

    if seconds < 60:
        return f"{seconds:.2f} sec"

    minutes = int(seconds // 60)

    seconds = seconds % 60

    return f"{minutes} min {seconds:.2f} sec"


def calculate_statistics(samples: List[float]) -> Dict[str, float]:
    """
    Calculate benchmark statistics.

    Returns

    minimum

    maximum

    average

    median

    p95

    p99

    total samples
    """

    if not samples:

        return {
            "count": 0,
            "min": 0,
            "max": 0,
            "average": 0,
            "median": 0,
            "p95": 0,
            "p99": 0,
        }

    samples = sorted(samples)

    count = len(samples)

    p95_index = int(count * 0.95)

    p99_index = int(count * 0.99)

    return {

        "count": count,

        "min": min(samples),

        "max": max(samples),

        "average": statistics.mean(samples),

        "median": statistics.median(samples),

        "p95": samples[p95_index],

        "p99": samples[p99_index],
    }


def print_section(title: str):
    """
    Print a formatted benchmark section.

    Example

    ==========================================
    LATENCY BENCHMARK
    ==========================================
    """

    print()

    print("=" * 70)

    print(title.center(70))

    print("=" * 70)


def print_metric(name: str, value):
    """
    Pretty print one metric.
    """

    print(f"{name:<30}: {value}")


def print_statistics(stats: Dict[str, float]):
    """
    Pretty print benchmark statistics.
    """

    print_metric("Samples", stats["count"])

    print_metric("Average", f"{stats['average']:.3f} ms")

    print_metric("Median", f"{stats['median']:.3f} ms")

    print_metric("Minimum", f"{stats['min']:.3f} ms")

    print_metric("Maximum", f"{stats['max']:.3f} ms")

    print_metric("P95", f"{stats['p95']:.3f} ms")

    print_metric("P99", f"{stats['p99']:.3f} ms")


if __name__ == "__main__":

    print_section("COMMON BENCHMARK UTILITIES")

    timer = Timer()

    timer.start()

    time.sleep(0.1)

    elapsed = timer.stop()

    print_metric("Measured Time", format_duration(elapsed))

    print()

    sample = [

        2.2,
        2.4,
        2.8,
        3.1,
        2.7,
        2.6,
        2.9,
        3.0,
        2.5,
        2.8,
    ]

    stats = calculate_statistics(sample)

    print_statistics(stats)
