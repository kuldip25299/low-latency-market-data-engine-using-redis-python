"""
benchmark/metrics.py

Collects CPU, memory and system metrics for benchmark reports.

Author:
    Kuldip Awachar

Repository:
    low-latency-market-data-engine-using-redis-python
"""

from __future__ import annotations

import os
import platform
import time
from dataclasses import dataclass, asdict

import psutil


# ---------------------------------------------------------
# Data Model
# ---------------------------------------------------------

@dataclass
class SystemMetrics:
    """
    Snapshot of system metrics.
    """

    cpu_percent: float

    memory_mb: float

    process_memory_mb: float

    available_memory_mb: float

    cpu_count: int

    process_id: int

    platform: str

    python_version: str

    timestamp: str


# ---------------------------------------------------------
# Metrics Collector
# ---------------------------------------------------------

class MetricsCollector:
    """
    Collect CPU and memory metrics.

    Example

        collector = MetricsCollector()

        collector.start()

        # benchmark work

        metrics = collector.stop()
    """

    def __init__(self):

        self.process = psutil.Process(os.getpid())

        self._start_time = None

    def start(self):
        """
        Prepare CPU measurement.

        psutil calculates CPU utilization
        between two sampling points.
        """

        self._start_time = time.time()

        psutil.cpu_percent(interval=None)

    def stop(self) -> SystemMetrics:
        """
        Capture current metrics.
        """

        virtual_memory = psutil.virtual_memory()

        process_memory = self.process.memory_info().rss

        cpu = psutil.cpu_percent(interval=0.2)

        return SystemMetrics(

            cpu_percent=cpu,

            memory_mb=virtual_memory.used / (1024 * 1024),

            process_memory_mb=process_memory / (1024 * 1024),

            available_memory_mb=virtual_memory.available / (1024 * 1024),

            cpu_count=psutil.cpu_count(),

            process_id=os.getpid(),

            platform=platform.platform(),

            python_version=platform.python_version(),

            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        )


# ---------------------------------------------------------
# Utility Printer
# ---------------------------------------------------------

def print_metrics(metrics: SystemMetrics):
    """
    Pretty print metrics.
    """

    print()

    print("=" * 70)
    print("SYSTEM METRICS".center(70))
    print("=" * 70)

    print(f"{'CPU Usage':30}: {metrics.cpu_percent:.2f} %")

    print(f"{'Process Memory':30}: {metrics.process_memory_mb:.2f} MB")

    print(f"{'System Memory Used':30}: {metrics.memory_mb:.2f} MB")

    print(f"{'Available Memory':30}: {metrics.available_memory_mb:.2f} MB")

    print(f"{'CPU Cores':30}: {metrics.cpu_count}")

    print(f"{'Process ID':30}: {metrics.process_id}")

    print(f"{'Python Version':30}: {metrics.python_version}")

    print(f"{'Platform':30}: {metrics.platform}")

    print(f"{'Timestamp':30}: {metrics.timestamp}")

    print("=" * 70)


# ---------------------------------------------------------
# Convert to dictionary
# ---------------------------------------------------------

def metrics_to_dict(metrics: SystemMetrics):
    """
    Used later for JSON reports.
    """

    return asdict(metrics)


# ---------------------------------------------------------
# Standalone Test
# ---------------------------------------------------------

if __name__ == "__main__":

    collector = MetricsCollector()

    collector.start()

    print("Generating CPU load...")

    data = []

    for i in range(1_000_000):
        data.append(i * i)

    metrics = collector.stop()

    print_metrics(metrics)