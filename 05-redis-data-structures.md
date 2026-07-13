# 🧱 Chapter 5: Choosing the Right Redis Data Structures

> **Goal of this chapter**
>
> By now we understand why Redis improves our architecture.
>
> However, Redis provides many different data structures:
>
> - String
> - Hash
> - List
> - Set
> - Sorted Set
> - Streams
> - Pub/Sub
>
> Choosing the wrong one can make your system harder to scale and maintain.
>
> In this chapter we'll learn **how to choose the right Redis data structure based on the business problem**, not just because a tutorial says so.

---

# Think Like an Engineer

One of the biggest mistakes new developers make is asking:

> Which Redis data structure is the best?

A better question is:

> Which Redis data structure best solves **this business problem?**

Every Redis data structure exists because it solves a different problem.

There is no "best" data structure.

There is only the **right data structure for the right use case**.

---

# Business Requirement #1

We receive this market update.

```
NIFTY

Price = 25,540

Volume = 1,200,000

High = 25,580

Low = 25,490
```

Question

How should we store this?

---

# Option 1 — String

We could store

```
Key

market:NIFTY

Value

25540
```

Looks simple.

Updating the latest price is easy.

```
SET market:NIFTY 25541
```

Reading the price is also easy.

```
GET market:NIFTY
```

---

## Problem

Where do we store

- Volume
- High
- Low
- Open
- Close

Do we create

```
market:NIFTY:price

market:NIFTY:volume

market:NIFTY:high

market:NIFTY:low
```

Now one symbol becomes many Redis keys.

Managing thousands of symbols becomes difficult.

---

# Better Option — Hash

Instead

we can store everything together.

```
market:NIFTY

------------------------

price

25540

volume

1200000

high

25580

low

25490

open

25500
```

Everything belongs to one market object.

Updating only the price

```
HSET market:NIFTY price 25541
```

Updating volume

```
HSET market:NIFTY volume 1300000
```

Reading everything

```
HGETALL market:NIFTY
```

Much cleaner.

---

# Why Hash Is Better

Imagine

```
5000 symbols
```

Each symbol has

```
10 fields
```

Using Strings

```
5000 × 10

=

50,000 keys
```

Using Hashes

```
5000 keys
```

Cleaner.

Easier to manage.

Less memory overhead.

This is why we'll use **Hashes** for storing the latest market state.

---

# Business Requirement #2

Now imagine

the Dashboard,

Strategy Engine,

Analytics,

Alert Engine,

all need to know

the instant a price changes.

Should they continuously ask Redis?

```
GET

GET

GET

GET

GET
```

No.

That is polling again.

We just moved polling from MySQL to Redis.

Polling is still inefficient.

---

# Better Solution — Pub/Sub

Instead

the Producer publishes new prices.

```
Producer

↓

Redis

↓

Dashboard

↓

Strategy

↓

Analytics

↓

Alert
```

Nobody asks

> Has the price changed?

Redis immediately pushes the update.

This is called

**Publish/Subscribe (Pub/Sub).**

---

# How Pub/Sub Works

Producer

```
PUBLISH market_updates

{
    symbol: NIFTY,
    price:25541
}
```

Subscribers

```
SUBSCRIBE market_updates
```

As soon as Redis receives a message,

every subscriber receives it instantly.

---

# Why Pub/Sub?

Without Pub/Sub

```
Dashboard

↓

GET

↓

Redis
```

every second.

With Pub/Sub

```
Redis

↓

Dashboard
```

No polling.

Lower latency.

Lower CPU usage.

Fewer network requests.

---

# Business Requirement #3

Exchange sends

```
5000

market updates
```

every second.

Should we execute

```
5000

HSET
```

commands individually?

No.

Each command requires

```
Application

↓

Redis

↓

Application
```

One network round trip.

---

# Better Solution — Pipelines

Redis Pipeline allows us to send many commands together.

Instead of

```
HSET

↓

HSET

↓

HSET

↓

HSET
```

we send

```
Pipeline

↓

100 Commands

↓

One Network Call
```

This greatly improves throughput.

---

# Why Pipelines Matter

Imagine

```
1000 updates
```

Without Pipeline

```
1000 Network Trips
```

With Pipeline

```
1 Network Trip

↓

1000 Commands
```

The Redis server still executes every command,

but the network overhead becomes much smaller.

---

# Business Requirement #4

Should we store market updates in a List?

```
LPUSH

Market Update
```

Technically yes.

But think about the business problem.

Do we need

every historical update?

No.

Our Dashboard only needs

```
Latest Price
```

Old prices are no longer useful.

A List keeps growing forever.

That wastes memory.

So we don't use Lists.

---

# Business Requirement #5

Should we use Redis Streams?

Streams are excellent when

every consumer must process

every event.

Example

```
Payment Created

↓

Notification Service

↓

Billing Service

↓

Audit Service
```

Every event is important.

Market data is different.

Suppose prices changed

```
25540

↓

25541

↓

25542

↓

25543
```

Dashboard only needs

```
25543
```

It doesn't care about every intermediate price.

For this project,

Streams add unnecessary complexity.

---

# Business Requirement #6

Should we use Sorted Sets?

Sorted Sets are useful for

```
Top Gainers

Top Losers

Leaderboard

Ranking
```

Our project doesn't require ranking.

So we won't use them.

---

# Final Decision

| Business Problem | Redis Feature | Why |
|------------------|--------------|-----|
| Store latest market state | Hash | Groups related fields together |
| Notify consumers instantly | Pub/Sub | Pushes updates without polling |
| Update thousands of symbols efficiently | Pipeline | Reduces network overhead |
| Store temporary values | String | Simple key/value storage |
| Historical event processing | Streams | Not required for this project |
| Ranking | Sorted Set | Not required for this project |

---

# Why Not Kafka?

Many readers might ask,

> Why not Kafka?

Kafka and Redis solve different problems.

Kafka is designed for

- Durable event streaming
- Event replay
- Long-term retention
- Large distributed event pipelines

Redis focuses on

- Extremely fast in-memory operations
- Shared application state
- Low-latency data access
- Lightweight message distribution

For this project,

our primary requirement is

> Deliver the latest market price as quickly as possible.

Redis is a better fit.

---

# Redis Features We'll Implement

Throughout this repository we'll build

✅ Latest Price Cache using Redis Hashes

✅ Real-Time Market Distribution using Pub/Sub

✅ Batch Updates using Pipelines

✅ Performance Benchmarks

✅ Multi-Consumer Architecture

Every Redis feature directly maps to a business requirement.

Nothing is added simply because Redis supports it.

---

# Key Takeaways

By now you should understand:

- There is no "best" Redis data structure.
- Every Redis feature solves a different engineering problem.
- Hashes are ideal for storing the latest market snapshot.
- Pub/Sub eliminates polling and enables real-time updates.
- Pipelines reduce network overhead when processing large numbers of updates.
- Streams, Lists, and Sorted Sets are powerful, but they are not the right choice for this particular architecture.

In the next chapter, we'll stop discussing architecture and start building the system from scratch using Python and Redis.
