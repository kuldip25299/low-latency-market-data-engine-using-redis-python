# Running the Project

This guide explains how to run the complete Redis Market Data Engine and verify every component is working correctly.

---

# System Architecture

```
                   +----------------------+
                   | Exchange Simulator   |
                   +----------+-----------+
                              |
                              v
                    +----------------------+
                    | Market Publisher     |
                    +----------+-----------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
       +----------------+            +----------------+
       | Redis Hash     |            | Redis Pub/Sub  |
       | Latest Prices  |            | Live Updates   |
       +----------------+            +----------------+
                |                             |
                |                             |
                +-------------+---------------+
                              |
                              v
                    +----------------------+
                    | Live Dashboard       |
                    +----------------------+
```

---

# Step 1 - Clone Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY>

cd low-latency-market-data-engine-using-redis-python
```

---

# Step 2 - Create Virtual Environment

macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

Windows

```cmd
python -m venv venv

venv\Scripts\activate
```

---

# Step 3 - Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Step 4 - Install Redis

macOS

```bash
brew install redis
```

Ubuntu

```bash
sudo apt install redis-server
```

---

# Step 5 - Start Redis

macOS

```bash
brew services start redis
```

Linux

```bash
sudo systemctl start redis
```

Verify Redis is running

```bash
redis-cli ping
```

Expected output

```
PONG
```

---

# Step 6 - Verify Redis Connection

```bash
python -m infrastructure.redis_client
```

Expected

```
Successfully connected to Redis.
```

---

# Step 7 - Verify Redis Hash

Run

```bash
python -m infrastructure.latest_price_cache
```

Open another terminal

```bash
redis-cli
```

Check stored data

```redis
KEYS market:*

HGETALL market:NIFTY
```

You should see the latest market data stored inside Redis Hash.

---

# Step 8 - Start Live Publisher

Open a new terminal.

Activate the virtual environment.

Run

```bash
python -m producer.market_publisher
```

This continuously generates simulated market data.

Leave this terminal running.

---

# Step 9 - Verify Pub/Sub

Open another terminal.

```bash
redis-cli
```

Subscribe

```redis
SUBSCRIBE market-data
```

You should immediately begin receiving JSON messages similar to:

```json
{
  "symbol": "NIFTY",
  "price": 25542.15,
  "high": 25560.00,
  "low": 25495.00,
  "volume": 420000,
  "timestamp": "2026-07-16T11:30:20"
}
```

This verifies Redis Pub/Sub is working correctly.

---

# Step 10 - Start Live Dashboard

Open another terminal.

Run

```bash
python -m consumer.dashboard
```

The dashboard should continuously update with the latest prices.

Example

```
============================================================
                 LIVE MARKET DASHBOARD
============================================================

Updated : 11:35:22 UTC

------------------------------------------------------------
Symbol         Price      High      Low       Volume
------------------------------------------------------------

INFY          1728.90   1740.00   1678.00     55210

NIFTY        25542.15  25560.00  25495.00    420000

RELIANCE      2966.90   2995.24   2955.94    101103

TCS           3893.52   3944.75   3885.90    104363
```

---

# Terminal Layout

The project is typically run using four terminals.

## Terminal 1

Redis Server

```bash
brew services start redis
```

---

## Terminal 2

Market Publisher

```bash
python -m producer.market_publisher
```

---

## Terminal 3

Redis Subscriber

```bash
redis-cli

SUBSCRIBE market-data
```

---

## Terminal 4

Dashboard

```bash
python -m consumer.dashboard
```

---

# What You Have Verified

By following the above steps, you have verified:

- Python successfully connects to Redis.
- Redis Hash stores the latest market state.
- Redis Pub/Sub broadcasts real-time market events.
- Market Publisher continuously publishes simulated exchange data.
- Dashboard receives live updates from Redis.
- Multiple applications communicate using Redis with low latency.

---

# Next Step

The next chapter benchmarks the Redis-based architecture against a traditional polling architecture to quantify improvements in latency, throughput, CPU usage, and memory consumption.