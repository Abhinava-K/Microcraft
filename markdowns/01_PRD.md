# Product Requirements Document (PRD)
## AI-Powered Investment Advisor Platform

### 1. Overview
This product is a personalized AI investment advisor that helps users make smarter investment decisions across two asset classes — Mutual Funds and Cryptocurrency. Unlike traditional investment dashboards that only display data, this platform actively analyzes user inputs and real-time market data to generate optimized, personalized portfolio recommendations.

### 2. Problem Statement
Most investment apps treat all users the same way. A 20-year-old and a 45-year-old with identical risk appetites receive identical portfolio suggestions, even though their time horizons, financial goals, and risk capacities differ significantly. Similarly, crypto investment guidance rarely accounts for volatility-adjusted optimization based on real historical data.

### 3. Goals and Objectives
- Provide age-aware, risk-aware, and duration-aware mutual fund portfolio recommendations.
- Provide volatility-and-return-optimized crypto portfolio recommendations.
- Use real, live market data rather than static or hardcoded suggestions.
- Offer an AI agent mode that lets users ask natural language investment questions and receive dynamic, data-backed answers.
- Demonstrate "thinking before recommending" — i.e., decisions are derived from logic and data, not generic templates.

### 4. Target Users
- Retail investors exploring SIPs (Systematic Investment Plans) and mutual funds.
- Crypto-curious investors seeking a structured, risk-adjusted approach.
- Hackathon judges and evaluators assessing innovation in personalized fintech and AI agent integration.

### 5. Core Modules

#### 5.1 Mutual Fund Module
**Inputs:**
- Age
- Investment amount
- Risk preference (Low / Medium / High)
- Investment duration (years)

**Processing:**
- Fetch live mutual fund data (NAV, category, historical performance) from MFAPI.
- Apply an age-based and duration-based allocation model to determine the equity/debt/hybrid mix.
- Rank and select top-performing funds within each category based on historical returns and consistency.
- Generate a rebalancing schedule that shifts allocation toward safer assets as the investment horizon shortens.

**Outputs:**
- Top 3 recommended funds with fund house names (e.g., HDFC, SBI).
- Allocation percentages across fund categories.
- Expected return projections (based on historical CAGR).
- Multi-phase rebalancing plan over the investment duration.

**Advanced Mode (AI Agent):**
- Users type natural language queries (e.g., "Suggest best SIP for 10 years under medium risk").
- The agent interprets intent, calls relevant APIs, and returns a dynamically generated comparison table.

#### 5.2 Crypto Portfolio Module
**Inputs:**
- Investment amount
- Risk preference (Low / Medium / High)

**Processing:**
- Fetch live and historical price/volatility data from CoinGecko API.
- Apply a risk-adjusted allocation model (e.g., mean-variance style logic) across major assets and stablecoins.
- Calculate expected return simulations and risk metrics (volatility, drawdown).

**Outputs:**
- Portfolio allocation percentages (e.g., BTC, ETH, SOL, Stablecoins).
- Expected return simulation (best/average/worst case).
- Risk analysis summary based on historical volatility.

**Advanced Mode (AI Agent):**
- Users type natural language queries (e.g., "How should I invest ₹50,000 in crypto for high returns?").
- The agent analyzes live market data and responds with a recommendation table.

### 6. Differentiators
- Age-based dynamic rebalancing logic for mutual funds (not static allocation).
- Volatility/return-driven optimization for crypto.
- Conversational AI agent layered on top of real-time financial APIs.
- Personalized, explainable recommendations rather than generic dashboards.

### 7. Success Metrics (for Hackathon Demo)
- Correct, distinct portfolio outputs for different user profiles (age/risk/duration combinations).
- Functional live API integration (MFAPI, CoinGecko) with real data shown in the UI.
- Working AI agent that answers at least 2–3 representative natural language queries with accurate, formatted tables.
- Clear visual presentation of allocation, projections, and rebalancing plan.

### 8. Out of Scope (for initial version)
- Real transaction execution (no actual buying/selling of funds or crypto).
- User authentication and persistent account management (optional/stretch goal).
- Tax computation and regulatory compliance features.
- Multi-currency support beyond INR/USD basics.

### 9. Assumptions
- MFAPI and CoinGecko free-tier APIs provide sufficient data for demo purposes.
- Allocation models are based on simplified, transparent heuristics suitable for a hackathon timeframe, with potential for more advanced optimization (e.g., Modern Portfolio Theory) as a stretch goal.
- The AI agent uses an LLM (e.g., Claude API) with tool-calling capability to fetch and reason over live data.

### 10. Risks and Mitigations
| Risk | Mitigation |
|---|---|
| API rate limits or downtime | Cache responses; use fallback sample data for demo |
| Inaccurate/oversimplified financial logic | Clearly label as "educational/demo purposes, not financial advice" |
| AI agent giving inconsistent answers | Constrain agent with structured prompts and validated data sources |
| Scope creep across two modules | Prioritize core flows first, advanced AI agent as secondary milestone |
