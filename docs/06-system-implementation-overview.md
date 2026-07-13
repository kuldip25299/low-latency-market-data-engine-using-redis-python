# 🏗️ Chapter 6: System Implementation Overview

> **Goal of this chapter**
>
> We've spent the previous chapters understanding the business problem and designing the architecture.
>
> Before writing any code, let's clearly define **what we are going to build**, how each component interacts, and why every component exists.
>
> Think of this chapter as the blueprint of our system.

---

# What Are We Building?

We are building a simplified version of a **Low-Latency Market Data Distribution System**.

Our application will simulate how market data flows inside a modern trading platform.

This is **not** an order matching engine.

This is **not** a trading platform.

Instead, we're focusing on one critical subsystem:

> **Distributing market data to multiple consumers with minimal latency.**

---

# High-Level Architecture

```
                        Exchange
                           │
                           ▼
                 Exchange Simulator
                           │
                           ▼
                 Market Data Producer
                           │
                           ▼
                  Redis (In-Memory)
                 ┌─────────┴─────────┐
                 ▼                   ▼
          Latest Price Cache      Pub/Sub
                 │                   │
      ┌──────────┼──────────┐        │
      ▼          ▼          ▼        ▼
 Dashboard   Strategy   Analytics   Alerts
```

Every component has a single responsibility.

---

# Component 1 – Exchange Simulator

Since we don't have access to a real stock exchange, we'll build our own.

Its responsibilities are:

- Generate market prices
- Simulate random price movement
- Publish updates continuously
- Read symbols from a CSV file

Example output:

```
NIFTY -> 25,540

TCS -> 3,925

RELIANCE -> 2,985
```

Think of this as our "fake NSE."

---

# Component 2 – Market Data Producer

The Producer acts as the gateway between the exchange and Redis.

Responsibilities:

- Receive market ticks
- Validate data
- Update Redis Hashes
- Publish updates to subscribers

Flow:

```
Exchange

↓

Producer

↓

Redis
```

Notice something important.

The Producer **does not know** who consumes the data.

Its only responsibility is to publish updates.

This loose coupling is one of the biggest advantages of event-driven architectures.

---

# Component 3 – Redis

Redis has two responsibilities in our system.

## Responsibility 1 – Store the Latest Market State

Example:

```
market:NIFTY

price = 25,540

volume = 1,200,000

high = 25,580

low = 25,490
```

This allows any service to instantly retrieve the current state.

---

## Responsibility 2 – Notify Consumers

Whenever the Producer publishes a new price:

```
NIFTY -> 25,541
```

Redis immediately broadcasts the update using Pub/Sub.

Every subscriber receives it simultaneously.

---

# Component 4 – Dashboard

The Dashboard represents a frontend application.

Responsibilities:

- Subscribe to market updates
- Display the latest prices
- Never query MySQL
- React immediately to new ticks

In our demo, the dashboard simply prints updates to the console.

Later, it could easily be replaced with a web application.

---

# Component 5 – Strategy Engine

The Strategy Engine represents an algorithmic trading system.

Responsibilities:

- Listen for price updates
- Apply trading rules
- Detect buy/sell signals

Example:

```
IF

Price > Moving Average

THEN

Generate BUY Signal
```

For simplicity, we'll implement only a few basic rules.

The goal is to demonstrate how strategies consume live market data.

---

# Component 6 – Analytics Engine

The Analytics Engine continuously calculates statistics such as:

- Price changes
- Moving averages
- Volume metrics
- Daily highs/lows

Instead of querying the database every few seconds, it receives updates directly from Redis.

---

# Component 7 – Alert Engine

The Alert Engine watches for user-defined conditions.

Example:

```
Alert me

when

NIFTY > 25,600
```

Whenever Redis publishes a new price, the Alert Engine immediately evaluates the condition.

No polling required.

---

# Why Multiple Consumers?

One Producer.

Many Consumers.

```
               Producer
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼

 Dashboard   Strategy   Analytics

        ▼          ▼          ▼

 Alerts     Future Services
```

Adding a new consumer should never require changes to the Producer.

This principle makes the architecture highly extensible.

---

# Why Are We Not Reading from MySQL?

One question many readers might ask is:

> Why don't consumers simply read from the database?

Because we've already learned:

- Databases are excellent for persistence.
- Redis is better suited for distributing rapidly changing data.

In our implementation:

- Redis provides the latest market state.
- MySQL (or another relational database) would be responsible for long-term storage.

Separating these responsibilities keeps each technology focused on what it does best.

---

# Project Directory

```
producer/

    exchange_simulator.py

    market_publisher.py

consumer/

    dashboard.py

    strategy_engine.py

    analytics_engine.py

    alert_engine.py

redis/

    redis_client.py

    publisher.py

    subscriber.py

    latest_price_cache.py

    pipelines.py
```

Each folder represents one part of the architecture we've discussed throughout this repository.

---

# Data Flow

Let's follow a single market update through the system.

```
Exchange

↓

NIFTY = 25,540

↓

Producer

↓

Redis Hash Updated

↓

Redis Pub/Sub Message

↓

Dashboard Updated

↓

Strategy Evaluated

↓

Analytics Calculated

↓

Alert Checked
```

Every component reacts independently.

No component needs to know about the internal logic of another.

---

# What We'll Build Next

Now that the architecture is complete, the remaining chapters become implementation-focused.

We'll build:

- Redis connection manager
- Exchange simulator
- Market publisher
- Latest price cache
- Redis Pub/Sub
- Dashboard subscriber
- Strategy engine
- Analytics engine
- Alert engine
- Performance benchmarks

Each module will be developed independently and then integrated into the complete system.

---

# Key Takeaways

After reading this chapter, you should understand:

- The overall architecture of the project.
- The responsibility of every component.
- How market data flows through the system.
- Why producers and consumers are loosely coupled.
- Why Redis sits between the producer and downstream services.
- What we'll implement in the codebase over the next chapters.

You now have a complete understanding of the system's design. The next step is to implement it and measure its performance under different workloads.
