---

We are building an AI-powered investment advisor website with two modules: Mutual Funds and Crypto Portfolio Optimization.

1. Mutual Fund Module

Problem:

Most investment apps give generic advice. But a 20-year-old and a 45-year-old with the same risk appetite should not get the same portfolio.

Our solution:

The user enters:

Age

Investment amount

Risk preference (low, medium, high)

Investment duration


The system then creates an optimized portfolio using real mutual fund data from providers like [MFAPI](https://www.mfapi.in?utm_source=chatgpt.com).

It recommends allocation percentages across top-performing funds.

Example:

A 20-year-old with medium risk and 15 years:

50% Equity Fund

30% Midcap Fund

20% Debt Fund


A 45-year-old with the same medium risk:

First 5 years:

40% Equity

20% Hybrid

40% Debt


Later years, portfolio automatically shifts toward safer assets.

So instead of static recommendations, we do age-based portfolio optimization and future rebalancing.

Output:

Top 3 recommended funds (for example from HDFC Mutual Fund or SBI Mutual Fund)

Allocation percentages

Expected return projections

Rebalancing plan over time


Advanced mode:

An AI agent where users can type questions.

Example:

“Suggest best SIP for 10 years under medium risk”

The agent calls APIs and dynamically generates relevant comparison tables.


---

2. Crypto Module

Problem:

Crypto is too volatile, so age-based planning doesn’t work like mutual funds.

Our solution:

The user enters:

Investment amount

Risk preference


Using market data from APIs like [CoinGecko API](https://www.coingecko.com/en/api?utm_source=chatgpt.com), the system builds an optimized crypto portfolio.

Example:

Medium risk:

45% Bitcoin

30% Ethereum

15% Solana

10% Stablecoins


Instead of age-based logic, we use historical return and volatility data to maximize returns while controlling risk.

Output:

Portfolio allocation percentages

Expected return simulations

Risk analysis based on historical data


Advanced mode:

AI agent for natural language queries.

Example:

“How should I invest ₹50,000 in crypto for high returns?”

Agent analyzes live market data and returns recommendations in table format.


---

Why this project stands out

Most finance apps only display data.

We are building a system that thinks before recommending.

It combines:

Real-time API integration

AI agents for custom financial advice

Personalized portfolio optimization

Dynamic asset allocation based on real-world financial logic


This is not a finance dashboard.

It is a personalized AI investment advisor that behaves differently for every user and optimizes decisions instead of giving generic suggestions.


---

For hackathon positioning, this is much stronger than a normal “investment tracker” website.