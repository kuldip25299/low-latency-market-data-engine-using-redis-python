# 🚀 Building a Low-Latency Market Data Distribution System using Redis & Python

## Understanding How Redis Enables Real-Time Market Data Distribution

---

# 📖 Overview

Modern financial applications continuously receive market data from exchanges. These updates must be distributed to dashboards, trading strategies, analytics services, and other downstream applications with minimal latency.

A common approach is allowing every service to repeatedly query a database for the latest market prices. While this works for small systems, it becomes increasingly inefficient as the number of consumers and update frequency grows.

This repository demonstrates how Redis can be used as an **in-memory data store** and **Publish/Subscribe messaging system** to distribute live market data efficiently.

> **Note:** This project is intentionally educational. It is designed to explain the architectural concepts behind Redis in low-latency systems rather than implement a production-grade trading platform.

---

# 🎯 Business Problem

Imagine an exchange continuously publishing market prices.

```text
Exchange

↓

Market Updates
```

Several applications require the latest prices.

* Trading Dashboard
* Strategy Engine
* Analytics Service
* Alert Engine
* Mobile Application

A traditional implementation stores every update in a database, and each application repeatedly queries the latest price.

```text
               Exchange
                   │
                   ▼
              Database
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Dashboard   Analytics   Strategy
        │          │          │
        └──────Repeated Queries───────┘
```

As more consumers are added, the database becomes responsible for serving the same information repeatedly.

---

# 🚨 Challenges with Traditional Architecture

As traffic increases, several issues appear.

* Repeated database polling
* Duplicate read operations
* Higher database CPU utilization
* Increased response latency
* More concurrent database connections
* Poor scalability
* Increased infrastructure cost

The bottleneck shifts from business logic to the database.

---

# ✅ Redis-Based Solution

Instead of allowing every consumer to poll the database, a single publisher sends market updates to Redis.

Redis stores the latest market state and immediately distributes new updates to subscribed consumers.

```text
                 Exchange
                      │
                      ▼
             Market Publisher
                      │
                      ▼
                   Redis
          (Hashes + Pub/Sub)
              │           │
              ▼           ▼
      Latest Price     Live Updates
          Cache
              │
              ▼
         Dashboard Consumer
```

This architecture enables:

* Real-time message delivery
* Latest price caching
* Reduced database dependency
* Event-driven communication
* Improved scalability
* Cleaner system design

---

# 🏗 What This Project Implements

This repository includes a complete educational implementation of a Redis-based market data distribution system.

### Exchange Simulator

Generates simulated market ticks.

### Market Publisher

Receives market ticks and publishes them to Redis.

### Redis Hashes

Stores the latest market state for every symbol.

Example:

```text
market:NIFTY
market:TCS
market:RELIANCE
```

### Redis Pub/Sub

Broadcasts every market update to subscribed consumers.

### Dashboard Consumer

Receives live updates directly from Redis and displays the latest market data.

### Redis Connection Pool

Uses a shared Redis connection pool for efficient communication.

---

# 📂 Repository Structure

```text
low-latency-market-data-engine-using-redis-python/

├── config/
│   Application configuration
│
├── producer/
│   Exchange Simulator
│   Market Publisher
│
├── infrastructure/
│   Redis Client
│   Publisher
│   Subscriber
│   Latest Price Cache
│
├── consumer/
│   Dashboard Consumer
│
├── models/
│   Market Tick model
│
├── docs/
│   Complete learning documentation
│
├── benchmark/
│   Reserved for future benchmarks
│
├── docker-compose.yml
│
└── main.py
```

---

# 🧠 Redis Concepts Covered

This project demonstrates:

* Redis Connection Pooling
* Redis Hashes
* Redis Pub/Sub
* Event-Driven Architecture
* Latest Price Cache Pattern
* Producer–Consumer Architecture
* Real-Time Market Data Distribution

---

# 📚 Documentation

The repository is organized as a step-by-step learning guide.

| Chapter | Description                        |
| ------- | ---------------------------------- |
| 00      | Redis Glossary                     |
| 01      | Business Problem                   |
| 02      | Traditional Architecture           |
| 03      | Why Traditional Architecture Fails |
| 04      | Redis Architecture                 |
| 05      | Redis Data Structures              |
| 06      | System Implementation Overview     |
| 07      | Production Considerations          |
| 08      | Running the Project                |
| 09      | Project Verification Guide         |
| 10      | Project Summary                    |

---

# 🚀 Features

* ✅ Exchange Simulator
* ✅ Market Publisher
* ✅ Redis Connection Pool
* ✅ Redis Hash Cache
* ✅ Redis Pub/Sub
* ✅ Dashboard Consumer
* ✅ Real-Time Market Updates
* ✅ Docker Support
* ✅ Step-by-Step Documentation
* ✅ Beginner-Friendly Architecture

---

# 🎓 What You Will Learn

After completing this project, you will understand:

* Why traditional polling architectures struggle to scale
* How Redis distributes live market data
* How Redis Hashes store the latest market state
* How Redis Pub/Sub works
* How producers and consumers communicate
* How event-driven systems reduce unnecessary polling
* How Redis fits into low-latency system design
* Practical Redis usage with Python

---

# 🛠 Technologies Used

* Python 3
* Redis
* Docker Compose
* redis-py
* Dataclasses
* Logging

---

# ▶️ Quick Start

Start Redis.

```bash
docker compose up -d
```

Run the Market Publisher.

```bash
python -m producer.market_publisher
```

Open another terminal and start the Dashboard.

```bash
python -m consumer.dashboard
```

Inspect Redis.

```bash
redis-cli
```

View cached prices.

```redis
HGETALL market:NIFTY
```

Subscribe to live updates.

```redis
SUBSCRIBE market-data
```

---

# ⭐ Why This Repository?

This repository is **not another Redis CRUD tutorial**.

Instead, it explains:

* Why traditional polling architectures become bottlenecks
* Why Redis is widely used for real-time data distribution
* How Publish/Subscribe enables event-driven communication
* How Redis Hashes maintain the latest application state
* How to build a practical Redis-based market data pipeline in Python

The focus is on understanding the **business problem**, the **architecture**, and the **implementation**, making it valuable for backend developers, distributed systems enthusiasts, and engineers exploring low-latency application design.

---

# 🚀 Future Enhancements

Possible future extensions include:

* Dashboard improvements
* Additional consumers
* Redis Streams
* Redis Cluster
* Redis Sentinel
* WebSocket integration
* REST APIs
* Kafka integration
* Grafana monitoring
* End-to-end latency measurements
* Production deployment examples

---

## ⭐ If you found this project helpful, consider giving the repository a star and sharing it with others who are learning Redis, event-driven systems, and low-latency architecture.
