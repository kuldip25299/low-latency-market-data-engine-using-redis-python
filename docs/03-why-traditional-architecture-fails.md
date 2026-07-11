# ❌ Chapter 3: Why the Traditional Architecture Fails at Scale

> **Goal of this chapter**
>
> In the previous chapter, we designed a simple architecture where every market update is stored in a relational database, and every downstream service queries that database whenever it needs the latest price.
>
> This architecture works well for small systems.
>
> But what happens when the market opens, thousands of instruments start updating, and multiple applications request the same data simultaneously?
>
> Let's find out.

---

# A Small System Works Perfectly

Imagine your application receives updates for only **5 stocks**.

```
NIFTY
BANKNIFTY
RELIANCE
TCS
INFY
```

Each stock updates

```
1 time per second
```

Total updates

```
5 updates/sec
```

You have

- Dashboard
- Analytics

Only two consumers.

Database workload

```
Writes

5/sec

Reads

10/sec
```

Any modern database can easily handle this.

No problems.

---

# Now the Business Grows

Your company expands.

Instead of

```
5 symbols
```

you now support

```
5,000 symbols
```

Average market activity

```
20 ticks/sec
```

per symbol.

Let's calculate.

```
5,000

×

20

=

100,000

market updates/sec
```

Your Market Data Collector must now process

```
100,000 writes/sec
```

---

# New Internal Services

The company also builds more applications.

```
Dashboard

Strategy Engine

Risk Engine

Analytics

Alert Engine

PnL Engine

Web API

Mobile API

Reporting

Data Export
```

Total

```
10 consumers
```

Each consumer needs the latest price.

---

# Database Write Load

Every market update must first be written.

```
Exchange

↓

100,000 updates/sec

↓

Database
```

Database writes

```
100,000 writes/sec
```

Already a significant workload.

---

# Database Read Load

Now imagine

every consumer requests

the latest price.

```
10 consumers

×

100,000 updates

=

1,000,000 reads/sec
```

The database now processes

```
Writes

100,000/sec

+

Reads

1,000,000/sec
```

Total

```
1.1 Million Operations Every Second
```

---

# But Wait...

Look carefully.

How many different prices exist?

Suppose

```
NIFTY

25,540
```

Dashboard asks

```
SELECT last_price
```

Strategy asks

```
SELECT last_price
```

Analytics asks

```
SELECT last_price
```

Risk asks

```
SELECT last_price
```

Alert Engine asks

```
SELECT last_price
```

All of them receive

```
25,540
```

The database executed five separate queries...

to return exactly the same value.

This is duplicated work.

---

# Visualizing Duplicate Reads

```
                 Database

                     │

      ┌──────────────┼──────────────┐

      ▼              ▼              ▼

 Dashboard      Strategy      Analytics

      │              │              │

 SELECT         SELECT         SELECT

      │              │              │

      └──────────────┼──────────────┘

               Same Price
```

The workload grows,

but the data does not change.

---

# Polling Makes It Worse

Most traditional systems poll.

Example

Dashboard

```
Every 500 ms

↓

SELECT latest price
```

Strategy

```
Every 200 ms
```

Analytics

```
Every 1000 ms
```

Risk

```
Every 250 ms
```

Even if the price hasn't changed,

every application still queries the database.

The database keeps answering

the same question.

---

# Network Overhead

Every query involves

```
Application

↓

Network

↓

Database

↓

Network

↓

Application
```

Suppose one query takes

```
3 milliseconds
```

Now multiply that by

```
1,000,000 reads/sec
```

A significant amount of time is spent simply moving data across the network.

---

# Database Connections

Every service needs database connections.

```
Dashboard

↓

Database Connection
```

Strategy

↓

Another Connection

Analytics

↓

Another Connection

Risk

↓

Another Connection

More users

↓

More connections

Eventually,

the connection pool becomes exhausted.

Applications begin waiting for available connections.

Latency increases.

---

# CPU Utilization

Every SQL query requires work.

The database must

- Parse SQL
- Validate permissions
- Locate indexes
- Read pages
- Build a result
- Send a response

Even a simple query consumes CPU cycles.

Millions of identical queries waste valuable CPU resources.

---

# Disk I/O

Traditional databases are designed for durable storage.

Although modern databases cache data aggressively,

they still maintain transaction logs,

indexes,

checkpoints,

and persistence.

These operations increase I/O activity.

For real-time market data,

our primary requirement isn't persistence.

It's speed.

---

# Growing Latency

As database load increases,

response time also increases.

```
Low Traffic

↓

2 ms
```

```
Medium Traffic

↓

8 ms
```

```
High Traffic

↓

25 ms
```

```
Peak Market Hours

↓

80+ ms
```

Now every downstream system receives delayed prices.

---

# Why This Matters

Imagine a trading strategy.

```
IF

NIFTY > 25,550

BUY
```

Suppose

the real market reaches

```
25,551
```

but the strategy receives

```
25,547
```

because the database is overloaded.

The trade executes late.

Milliseconds matter.

---

# Horizontal Scaling Doesn't Completely Solve It

You might think,

"We'll just add another database server."

Unfortunately,

the problem remains.

Every consumer still performs

```
SELECT latest_price
```

Scaling hardware doesn't eliminate duplicate reads.

It only delays the bottleneck.

---

# The Core Problem

Let's summarize.

The database is doing three different jobs.

```
1.

Persisting Market Data

✓
```

```
2.

Serving Historical Queries

✓
```

```
3.

Distributing Live Market Data

❌
```

The third responsibility is where the architecture struggles.

A relational database is an excellent system of record.

It is not an ideal real-time message distribution platform.

---

# What Do We Actually Need?

Instead of every consumer repeatedly asking

```
"Has the price changed?"
```

Wouldn't it be better if

the latest price was immediately available

to everyone?

Instead of

```
Consumer

↓

Database

↓

Consumer

↓

Database

↓

Consumer

↓

Database
```

What if

new prices were distributed automatically

to every interested service?

That is exactly the architectural problem we solve in the next chapter.

---

# Key Takeaways

After reading this chapter, you should understand:

- Relational databases can become bottlenecks under heavy read and write workloads.
- Multiple services often request exactly the same market data.
- Polling creates unnecessary database traffic.
- Duplicate reads waste CPU, network bandwidth, and database connections.
- Increasing hardware capacity delays the problem but doesn't eliminate it.
- The real challenge is efficient **data distribution**, not simply storing data.

In the next chapter, we'll redesign the architecture and introduce Redis as an in-memory data distribution layer that dramatically reduces database load while enabling low-latency access to market data.
