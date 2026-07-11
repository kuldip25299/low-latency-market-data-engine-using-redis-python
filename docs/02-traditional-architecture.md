# 🏗️ Chapter 2: Traditional Database-Centric Architecture

> **Goal of this chapter**
>
> In the previous chapter, we learned that multiple services require the latest market prices in real time.
>
> A common first approach is to store every market update in a relational database and let every application query the database whenever it needs data.
>
> Let's understand how this architecture works before we analyze its limitations.

---

# The First Design Most Developers Build

Imagine you've been asked to build a trading platform.

You already know relational databases like MySQL or PostgreSQL.

Naturally, your architecture might look like this.

```
                Exchange
                    │
                    ▼
          Market Data Collector
                    │
                    ▼
                 MySQL Database
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 Dashboard     Strategy Engine   Analytics
      ▼             ▼             ▼
 Alert Engine    Mobile API     Risk Engine
```

This architecture is simple.

It is also the architecture many teams start with.

---

# Step 1 – Market Data Arrives

Suppose the exchange publishes

```
NIFTY

25,540
```

Your Market Data Collector receives it.

```
Exchange

↓

Market Data Collector

↓

Price Received
```

---

# Step 2 – Store the Latest Price

The application writes the market update into MySQL.

```sql
UPDATE market_data
SET
    last_price = 25540,
    volume = 125000,
    updated_at = NOW()
WHERE symbol='NIFTY';
```

Now the database contains

| Symbol | Price |
|---------|------:|
| NIFTY | 25,540 |
| TCS | 3,925 |
| INFY | 1,682 |

Everything seems fine.

---

# Step 3 – Consumers Need Data

Now different services need the latest market price.

For example,

Dashboard

```sql
SELECT last_price
FROM market_data
WHERE symbol='NIFTY';
```

Strategy Engine

```sql
SELECT last_price
FROM market_data
WHERE symbol='NIFTY';
```

Analytics

```sql
SELECT last_price
FROM market_data
WHERE symbol='NIFTY';
```

Risk Engine

```sql
SELECT last_price
FROM market_data
WHERE symbol='NIFTY';
```

Notice something interesting.

Every service is requesting **the exact same value**.

---

# What Happens Next?

Every consumer continues polling the database.

```
Dashboard

↓

SELECT

↓

Database

↓

Dashboard

↓

SELECT

↓

Database
```

The Strategy Engine does the same.

The Analytics Engine does the same.

The Alert Service does the same.

The Mobile API does the same.

Every service continuously asks:

> "Has the price changed?"

---

# Visualizing the Architecture

```
                    Exchange
                        │
                        ▼
                Market Data Collector
                        │
                        ▼
                 ┌────────────┐
                 │   MySQL    │
                 └────────────┘
                  ▲    ▲    ▲
                  │    │    │
      ┌───────────┘    │    └──────────────┐
      ▼                ▼                   ▼

 Dashboard      Strategy Engine      Analytics

      ▲                ▲                   ▲
      │                │                   │

   Repeated        Repeated          Repeated
    Queries         Queries           Queries
```

The database becomes the center of everything.

---

# Example Timeline

Imagine one market update arrives.

```
09:15:00.000

NIFTY

25,540
```

Immediately,

Dashboard requests the price.

```
SELECT last_price
```

Strategy Engine requests the price.

```
SELECT last_price
```

Analytics requests the price.

```
SELECT last_price
```

Alert Engine requests the price.

```
SELECT last_price
```

Five consumers.

Five queries.

One price.

---

# Scaling the Example

Suppose we have

```
5,000 symbols
```

Each symbol updates

```
20 times per second
```

That means

```
100,000

market updates

every second
```

Now imagine

```
20
```

internal services.

Each service requests the latest price.

The database suddenly receives millions of read operations.

---

# Why Developers Like This Architecture

At first, this design looks attractive.

✅ Easy to understand

✅ Simple SQL queries

✅ Centralized storage

✅ Reliable relational database

✅ Familiar technology

For a small application, this works perfectly.

---

# Where This Architecture Works Well

This architecture is perfectly acceptable when:

- Market updates are infrequent.
- Only one or two services need the data.
- User traffic is low.
- Latency is not critical.
- Data changes only occasionally.

Examples include:

- Admin dashboards
- Reporting systems
- Inventory management
- Employee portals

There is nothing wrong with using a relational database in these scenarios.

---

# But Trading Systems Are Different

Trading systems have unique requirements.

Prices change continuously.

```
Exchange

↓

Tick

↓

Tick

↓

Tick

↓

Tick
```

Consumers cannot wait seconds for updates.

They require the latest information almost immediately.

As traffic increases,

the database becomes responsible for:

- Continuous writes from the exchange.
- Continuous reads from every consumer.
- Maintaining indexes.
- Managing connections.
- Executing SQL queries.
- Handling locks and transactions.

Eventually,

one database is responsible for serving the entire company.

---

# Is the Database the Right Tool?

Relational databases are excellent at:

- Persisting data
- Running complex queries
- Maintaining relationships
- Supporting transactions
- Ensuring data consistency

However,

our business problem is different.

We are not asking questions like:

> "Show me all trades from last month."

Instead,

we repeatedly ask:

> "What is the latest price of NIFTY?"

This is a very different workload.

The database is being used primarily as a **real-time data distribution system**, which is not what it was originally designed for.

---

# Common Misconception

Many developers assume:

```
Fast Database

=

Fast Application
```

In reality,

application performance depends on the entire architecture.

Even the fastest database becomes a bottleneck if thousands of services repeatedly request the same information.

Sometimes,

the problem is not the database itself.

The problem is **how we use it**.

---

# Key Takeaways

After reading this chapter, you should understand:

- A traditional architecture stores market data in a relational database.
- Every downstream service queries the same database.
- This design is simple and works well for small systems.
- As traffic increases, the database becomes the central dependency for every application.
- Using a database as a real-time distribution layer is not always the best architectural choice.

In the next chapter, we'll examine **why this architecture breaks down at scale**, quantify the bottlenecks, and understand the engineering challenges that lead teams to adopt technologies like Redis.
