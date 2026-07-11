# 📈 Chapter 1: Understanding the Business Problem

> **Goal of this chapter**
>
> Before learning Redis or writing any code, let's understand **why this project exists** and the real business problem we are trying to solve.

---

# Imagine You Work at a Stock Brokerage

You've just joined a company that provides an online trading platform similar to Zerodha, Groww, Robinhood, or Interactive Brokers.

Every trading day, your application receives continuous market updates from the stock exchange.

These updates include:

- Last traded price
- Best bid price
- Best ask price
- Trading volume
- Open price
- High price
- Low price

Every price change is called a **Market Tick**.

During market hours, the exchange continuously publishes new ticks.

```
09:15:00.100

NIFTY
Price = 25,540
```

```
09:15:00.135

NIFTY
Price = 25,541
```

```
09:15:00.160

NIFTY
Price = 25,539
```

This process never stops until the market closes.

---

# The Business Requirement

Your company doesn't have just one application.

It has many independent systems that all require the latest market price.

For example,

```
                    Exchange
                        │
                        ▼
                 Market Data Feed
                        │
      ┌─────────────────┼──────────────────┐
      ▼                 ▼                  ▼
 Dashboard       Strategy Engine     Alert Engine
      ▼                 ▼                  ▼
 Analytics         Risk Engine       Mobile App
```

Every service depends on the latest market price.

Let's understand why.

---

# Dashboard

The dashboard displays live prices to traders.

```
NIFTY

25,541
```

As soon as the market price changes,

the dashboard must immediately display

```
25,542
```

Any delay creates a poor user experience.

---

# Strategy Engine

Algorithmic trading strategies continuously monitor price movements.

Example:

```
IF

NIFTY > 25,550

THEN

BUY
```

If the strategy receives outdated prices,

it may execute trades too late.

Milliseconds matter.

---

# Alert Engine

Some users create price alerts.

Example

```
Notify me

when

TCS > ₹4000
```

The alert service continuously checks market prices.

If it receives delayed data,

users receive delayed notifications.

---

# Analytics Engine

The analytics system continuously calculates:

- Average price
- VWAP
- Moving Average
- High
- Low
- Daily Statistics

It also depends on the latest market updates.

---

# Risk Management

Risk systems monitor open positions.

Example

```
Current Position

↓

Current Market Price

↓

Current Profit/Loss

↓

Risk Exposure
```

Using outdated prices may produce incorrect risk calculations.

---

# Mobile Application

The mobile application also displays live prices.

Users expect to see the same market price on:

- Web
- Mobile
- Desktop

All at nearly the same time.

---

# A Simple Example

Suppose the exchange publishes this update.

```
RELIANCE

₹2,950
```

Immediately,

every internal service requires the same information.

```
                    RELIANCE

                     ₹2,950
                         │
 ┌──────────────┬─────────┼─────────────┬──────────────┐
 ▼              ▼         ▼             ▼              ▼

Dashboard   Strategy   Analytics    Alerts      Mobile App
```

Notice something.

Every system needs **exactly the same data**.

Only their processing logic differs.

---

# The Scale of the Problem

Now imagine the following numbers.

Exchange sends

```
1,000,000

Market Updates

Every Second
```

Your company has

- Dashboard
- Strategy Engine
- Analytics
- Alert Service
- Mobile API
- Web API
- Reporting
- Risk Management

Each one needs the latest prices.

This creates a massive data distribution problem.

---

# Why Is This Difficult?

Imagine just one stock.

```
NIFTY
```

Price changes

```
100

times

every second.
```

Now imagine

```
5,000
```

stocks.

Now imagine

```
100,000
```

users connected.

Now imagine

```
20
```

different internal services.

Every one of them requires the latest prices immediately.

The challenge is no longer collecting market data.

The real challenge is **distributing it efficiently**.

---

# What Does the Business Actually Need?

The business has several important requirements.

✅ Every consumer should receive the latest market price.

✅ Data should be available with minimal latency.

✅ Multiple services should be able to consume the same data simultaneously.

✅ The system should scale as the number of users grows.

✅ Infrastructure costs should remain reasonable.

✅ The architecture should support future expansion.

---

# Can We Simply Store Everything in a Database?

At first glance,

this seems like a reasonable solution.

```
Exchange

↓

Database

↓

Dashboard

↓

Strategy

↓

Analytics
```

Many beginner developers build systems exactly like this.

Unfortunately,

this architecture begins to fail as traffic increases.

We'll explore exactly **why** in the next chapter.

---

# Real-World Perspective

Large financial institutions process enormous volumes of market data every trading day.

Their challenge is not just storing information, but ensuring that multiple downstream systems receive the latest data with extremely low latency.

While every company has its own architecture, a common design principle is to use specialized technologies for **real-time data distribution** instead of relying solely on traditional relational databases.

This repository demonstrates one such architectural approach using Redis and Python.

---

# Key Takeaways

After reading this chapter, you should understand:

- Market exchanges continuously publish price updates.
- Multiple independent services require the same market data.
- Every service depends on receiving the latest prices quickly.
- As traffic grows, distributing market data becomes a significant engineering challenge.
- Choosing the right architecture is critical for building scalable, low-latency systems.

In the next chapter, we'll examine the **traditional database-centric architecture**, understand how it works, and explore why it becomes a bottleneck as systems scale.
