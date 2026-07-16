# Benchmark Guide

## Objective

Understanding Redis conceptually is important, but understanding **why Redis is used in low-latency systems** is even more valuable.

This project includes benchmarks that compare a traditional architecture with a Redis-based architecture using measurable performance metrics.

Instead of making assumptions, we collect real numbers.

---

# What We Are Comparing

## Traditional Architecture

```
Exchange
    │
    ▼
Application
    │
    ▼
Database
    │
    ▼
Dashboard (Polling every second)
```

Characteristics

- Dashboard continuously polls the database.
- Every client generates read queries.
- Increased database load.
- Higher response latency.
- Poor scalability.

---

## Redis Architecture

```
Exchange
      │
      ▼
Market Publisher
      │
      ▼
Redis
      │
 ┌────┴─────┐
 ▼          ▼
Hash      Pub/Sub
 │          │
 ▼          ▼
Latest    Dashboard
Price
```

Characteristics

- Database is no longer queried continuously.
- Redis stores the latest market snapshot.
- Dashboard receives updates instantly.
- Lower latency.
- Higher throughput.
- Better scalability.

---

# Why Benchmark?

Suppose someone asks:

> Why should I introduce Redis into my architecture?

Instead of saying

> "Redis is fast."

You can answer

> "Redis reduced average latency by 180x while lowering CPU utilization by more than 70%."

That is much more convincing.

---

# Metrics We Measure

This project benchmarks the following metrics.

---

## 1. Average Latency

Measures the average time taken for a market update to reach the consumer.

Lower is better.

Example

```
Traditional

520 ms

Redis

3 ms
```

---

## 2. Maximum Latency

Sometimes systems experience spikes.

Maximum latency tells us the slowest update observed during the benchmark.

Lower is better.

---

## 3. Throughput

Measures how many market updates can be processed every second.

Example

```
Traditional

1,000 ticks/sec

Redis

150,000 ticks/sec
```

Higher is better.

---

## 4. CPU Usage

Measures processor utilization while processing market updates.

Lower CPU means

- lower infrastructure cost
- better scalability
- more room for business logic

---

## 5. Memory Usage

Measures RAM consumed during processing.

This helps compare

- polling
- caching
- Pub/Sub

---

## 6. Network Calls

Traditional architecture

```
Dashboard

↓

SELECT price
```

repeated continuously.

Redis architecture

```
Publisher

↓

One Publish

↓

Many Subscribers
```

Network traffic is dramatically reduced.

---

# Benchmark Scenarios

The repository includes multiple benchmark scenarios.

---

## Benchmark 1

### Database Polling

Dashboard queries database every second.

Measures

- latency
- database load
- CPU usage

---

## Benchmark 2

### Redis Hash

Dashboard reads latest prices directly from Redis.

Measures

- lookup latency
- throughput
- CPU usage

---

## Benchmark 3

### Redis Pub/Sub

Dashboard receives market updates instantly.

Measures

- event latency
- publish throughput
- subscriber performance

---

## Benchmark 4

### Multiple Subscribers

One publisher

Many consumers

```
Publisher

↓

Redis

↓

Dashboard

↓

Analytics

↓

Alert Engine

↓

Strategy Engine
```

Demonstrates Redis scalability.

---

## Benchmark 5

### High Frequency Simulation

Generate

```
100,000

500,000

1,000,000
```

market ticks.

Measure

- processing time
- throughput
- memory usage

---

# Benchmark Output

Each benchmark prints a report similar to:

```
============================================================

REDIS BENCHMARK REPORT

============================================================

Duration

60 Seconds

--------------------------------------------

Total Market Updates

100000

--------------------------------------------

Average Latency

2.8 ms

--------------------------------------------

Maximum Latency

7.4 ms

--------------------------------------------

Throughput

154,280 ticks/sec

--------------------------------------------

CPU Usage

9%

--------------------------------------------

Memory Usage

13 MB

============================================================
```

---

# Traditional Benchmark Example

```
============================================================

DATABASE POLLING REPORT

============================================================

Average Latency

510 ms

Maximum Latency

1020 ms

Throughput

1,250 ticks/sec

CPU Usage

31%

Memory Usage

27 MB

============================================================
```

---

# Comparing Results

| Metric | Traditional Polling | Redis |
|----------|--------------------:|------:|
| Average Latency | 510 ms | 2.8 ms |
| Maximum Latency | 1020 ms | 7.4 ms |
| Throughput | 1,250 ticks/sec | 154,280 ticks/sec |
| CPU Usage | 31% | 9% |
| Memory Usage | 27 MB | 13 MB |

---

# Business Impact

The benchmark demonstrates why organizations use Redis in systems requiring real-time performance.

Examples include

- High Frequency Trading
- Stock Exchanges
- Cryptocurrency Exchanges
- Payment Systems
- Fraud Detection
- Real-Time Dashboards
- Online Gaming
- IoT Platforms
- Live Sports Scoreboards
- Chat Applications

---

# Key Takeaways

After completing the benchmarks, you should understand:

- Why database polling introduces unnecessary latency.
- Why Redis Hash is an efficient solution for serving the latest state.
- Why Redis Pub/Sub is ideal for distributing real-time events.
- How Redis reduces CPU usage and network traffic.
- How Redis enables applications to scale efficiently with multiple consumers.
- Why Redis is widely used in low-latency and high-throughput systems.

---
