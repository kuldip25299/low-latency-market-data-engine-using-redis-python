# 09. Project Verification Guide

# Verifying the Redis Market Data Distribution System

---

# Overview

This guide explains how to verify that every component of the project is working correctly.

Unlike traditional benchmarking, the goal of this project is to validate the Redis-based architecture and observe how market data flows through the system in real time.

By the end of this guide, you will verify:

* Redis connectivity
* Market data generation
* Latest Price Cache
* Redis Pub/Sub
* Dashboard updates
* Redis CLI inspection

---

# System Architecture

The complete flow of this project is shown below.

```text
                 Exchange Simulator
                        │
                        ▼
               Market Publisher
                        │
                        ▼
                 Redis Server
                ┌──────────────┐
                │              │
                ▼              ▼
         Redis Hashes     Redis Pub/Sub
                │              │
                └──────┬───────┘
                       ▼
                Dashboard Consumer
```

---

# Step 1 — Start Redis

Start Redis using Docker Compose.

```bash
docker compose up -d
```

Verify Redis is running.

```bash
docker ps
```

Expected output:

```text
redis
Up ...
```

---

# Step 2 — Verify Redis Connection

Run the Redis connection test.

```bash
python -m infrastructure.redis_client
```

Expected output:

```text
Redis Connection Test

Successfully connected to Redis.

Stored Value : Connection Successful

Redis connection is working correctly.
```

This confirms:

* Redis server is reachable
* Connection pool works
* Read/Write operations succeed

---

# Step 3 — Start the Market Publisher

Open a new terminal.

Run:

```bash
python -m producer.market_publisher
```

Expected output:

```text
Market Publisher started.

Tick received:
MarketTick(
    symbol='RELIANCE',
    price=2971.45,
    ...
)

Published to Redis.
```

The publisher continuously generates simulated market data.

---

# Step 4 — Verify Redis Hash Cache

Open another terminal.

Start Redis CLI.

```bash
redis-cli
```

List available market keys.

```redis
KEYS market:*
```

Expected output:

```text
market:NIFTY
market:TCS
market:INFY
market:RELIANCE
market:HDFCBANK
```

Inspect one symbol.

```redis
HGETALL market:NIFTY
```

Example output:

```text
symbol
NIFTY

price
25542.25

high
25560.00

low
25495.00

volume
245000

timestamp
2026-07-23T15:42:11
```

This verifies that the latest market state is stored correctly using Redis Hashes.

---

# Step 5 — Verify Redis Pub/Sub

While still inside Redis CLI:

```redis
SUBSCRIBE market-data
```

Expected output:

```text
1) "message"
2) "market-data"
3) {
     "symbol":"RELIANCE",
     "price":2968.40,
     ...
   }
```

New market updates should continuously appear.

This confirms:

* Publisher is sending messages
* Redis Pub/Sub is working
* Messages are delivered immediately

---

# Step 6 — Start Dashboard Consumer

Open another terminal.

Run:

```bash
python -m consumer.dashboard
```

Example output:

```text
==========================================================
 Live Market Dashboard
==========================================================

SYMBOL       PRICE      HIGH      LOW

RELIANCE     2968.45    2975.20   2958.10
TCS          3892.10    3901.30   3880.00
INFY         1729.50    1735.80   1721.60
```

The dashboard should update automatically as new market ticks arrive.

No manual refresh is required.

---

# Recommended Terminal Layout

For the best experience, use five terminals.

## Terminal 1

Start Redis.

```bash
docker compose up -d
```

---

## Terminal 2

Run Market Publisher.

```bash
python -m producer.market_publisher
```

---

## Terminal 3

Open Redis CLI.

```bash
redis-cli
```

Subscribe to market updates.

```redis
SUBSCRIBE market-data
```

---

## Terminal 4

Run Dashboard.

```bash
python -m consumer.dashboard
```

---

## Terminal 5

Inspect Redis Hashes.

```redis
redis-cli

KEYS market:*

HGETALL market:NIFTY
```

---

# What to Observe

While the project is running, notice the following:

✔ Market prices continuously change.

✔ Redis Hash always stores the latest price.

✔ Pub/Sub instantly broadcasts new messages.

✔ Dashboard updates automatically.

✔ No consumer polls the database.

✔ A single producer can serve multiple consumers.

---

# Manual Verification Checklist

| Feature            | Expected Result        | Status |
| ------------------ | ---------------------- | ------ |
| Redis Connection   | Connected successfully | ✅      |
| Exchange Simulator | Generates market ticks | ✅      |
| Market Publisher   | Publishes updates      | ✅      |
| Redis Hash Cache   | Latest prices stored   | ✅      |
| Redis Pub/Sub      | Messages received      | ✅      |
| Dashboard          | Live updates displayed | ✅      |

---

# Common Issues

## ModuleNotFoundError

Run Python modules using:

```bash
python -m infrastructure.redis_client
```

instead of:

```bash
python infrastructure/redis_client.py
```

---

## No Pub/Sub Messages

Verify that the configured channel matches.

For example:

```python
MARKET_DATA_CHANNEL = "market-data"
```

Publisher and subscriber must use the same channel name.

---

## No Redis Keys

Ensure the publisher is running.

```bash
python -m producer.market_publisher
```

The cache is populated only after market data starts publishing.

---

## Dashboard Not Updating

Check:

* Redis server is running.
* Publisher is active.
* Dashboard is connected to Redis.
* Channel names match.

---

# Learning Outcomes

After completing this verification guide, you will understand:

* How Redis stores live market data.
* How Redis Hashes maintain the latest state.
* How Redis Pub/Sub distributes messages.
* How producers and consumers communicate.
* How Redis enables event-driven architectures.

---

# Conclusion

This verification exercise demonstrates the complete flow of a simplified low-latency market data system.

Although this project is intentionally lightweight, it introduces the same architectural concepts used in larger distributed systems:

* Event-driven communication
* In-memory caching
* Publish/Subscribe messaging
* Decoupled producers and consumers

The focus of this repository is understanding **how Redis enables efficient real-time data distribution**, rather than comparing raw database performance.
