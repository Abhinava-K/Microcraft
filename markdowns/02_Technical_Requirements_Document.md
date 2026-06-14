# Technical Requirements Document (TRD)
## AI-Powered Investment Advisor Platform

### 1. System Architecture Overview
The platform follows a modular web application architecture with a frontend client, a backend API layer, an AI agent service, and integrations with external financial data providers.

**High-level components:**
- Frontend (Web UI)
- Backend API (business logic, allocation engines)
- AI Agent Service (LLM-powered, tool-calling)
- External Data Integrations (MFAPI, CoinGecko)
- Caching Layer (to manage rate limits and improve performance)
- Database (optional, for storing user sessions, query history, fund metadata)

### 2. Technology Stack (Suggested)

| Layer | Technology Options |
|---|---|
| Frontend | React.js (with Tailwind CSS), or Next.js for SSR |
| Backend | Node.js (Express) or Python (FastAPI) |
| AI Agent | Claude API (with tool use / function calling) |
| Database | PostgreSQL or MongoDB (optional for MVP) |
| Caching | Redis or in-memory cache for API responses |
| Hosting | Vercel/Netlify (frontend), Render/Railway/AWS (backend) |
| Charts/Visualization | Recharts, Chart.js, or D3.js |

### 3. Mutual Fund Module — Technical Details

#### 3.1 Data Source
- **MFAPI** (https://www.mfapi.in): provides scheme codes, NAV history, and fund metadata for Indian mutual funds.

#### 3.2 Allocation Engine Logic
- Input parameters: age, amount, risk preference, duration.
- Allocation logic determined by a rules-based matrix combining age bands, risk levels, and duration:
  - Age bands (e.g., <30, 30–45, 45–60, 60+)
  - Risk levels (Low, Medium, High)
  - Duration bands (e.g., <5 years, 5–10 years, 10+ years)
- Each combination maps to a target asset class mix (Equity %, Midcap %, Hybrid %, Debt %).
- Fund selection: for each asset class, query MFAPI for funds in that category, rank by historical CAGR/consistency over 3–5 years, and select the top fund(s).

#### 3.3 Rebalancing Engine
- Divide the total duration into phases (e.g., early phase, mid phase, final phase).
- For each phase, recalculate the target allocation using the same matrix but with an adjusted "effective age" (age + years elapsed).
- Output a timeline showing how allocation percentages shift across phases.

#### 3.4 Return Projection
- Use historical CAGR data per fund/category to project expected portfolio value at the end of the duration, using compound growth formulas.
- Present as a range (conservative, expected, optimistic) based on historical volatility bands.

#### 3.5 API Endpoints (Backend)

| Endpoint | Method | Description |
|---|---|---|
| `/api/mf/recommend` | POST | Accepts age, amount, risk, duration; returns allocation, top funds, projections, rebalancing plan |
| `/api/mf/funds` | GET | Returns list/details of mutual funds (proxied/cached from MFAPI) |
| `/api/mf/agent` | POST | Accepts natural language query; returns AI-generated comparison table |

### 4. Crypto Module — Technical Details

#### 4.1 Data Source
- **CoinGecko API** (https://www.coingecko.com/en/api): provides current prices, historical price data, market cap, and volatility-related metrics.

#### 4.2 Allocation Engine Logic
- Input parameters: investment amount, risk preference.
- Risk-based allocation templates (e.g., Low/Medium/High) define base weightings across categories: large-cap (BTC, ETH), mid-cap altcoins (e.g., SOL), and stablecoins.
- Optionally refine weights using historical volatility/return data fetched from CoinGecko (e.g., higher volatility assets get reduced weight in lower-risk profiles).

#### 4.3 Risk & Return Simulation
- Pull historical price data (e.g., last 1–3 years) for selected assets.
- Compute metrics: average return, standard deviation (volatility), max drawdown.
- Run a simple simulation (e.g., Monte Carlo or historical scenario replay) to generate best/average/worst case projections for the portfolio.

#### 4.4 API Endpoints (Backend)

| Endpoint | Method | Description |
|---|---|---|
| `/api/crypto/recommend` | POST | Accepts amount, risk; returns allocation, projections, risk analysis |
| `/api/crypto/market` | GET | Returns cached live market data from CoinGecko |
| `/api/crypto/agent` | POST | Accepts natural language query; returns AI-generated recommendation table |

### 5. AI Agent Service

#### 5.1 Design
- Built using an LLM (Claude API) with tool-calling/function-calling capability.
- Tools exposed to the agent:
  - `get_mutual_fund_data(category, filters)`
  - `get_crypto_market_data(coins, timeframe)`
  - `compute_allocation(profile)`
  - `compute_projection(portfolio, duration)`

#### 5.2 Flow
1. User submits a natural language query via chat interface.
2. Agent parses intent and required parameters (amount, duration, risk, asset type).
3. Agent calls appropriate backend tools/functions to fetch live data.
4. Agent synthesizes a structured response, typically a markdown/JSON table plus brief explanation.
5. Frontend renders the table and explanation.

#### 5.3 Guardrails
- System prompt constrains the agent to use only data returned by tools (no fabricated numbers).
- Disclaimers appended to all responses: "This is for educational purposes, not financial advice."

### 6. Caching & Rate Limit Management
- Cache MFAPI and CoinGecko responses (e.g., 15–60 minute TTL) to avoid repeated calls and handle rate limits.
- Implement fallback static/sample datasets in case live APIs are unavailable during demo.

### 7. Data Models (Simplified)

**User Profile Input (Mutual Fund)**
```json
{
  "age": 28,
  "amount": 100000,
  "risk": "medium",
  "duration_years": 15
}
```

**Mutual Fund Recommendation Output**
```json
{
  "allocation": {"equity": 50, "midcap": 30, "debt": 20},
  "top_funds": [
    {"name": "HDFC Equity Fund", "category": "equity", "cagr_3y": 14.2},
    {"name": "SBI Midcap Fund", "category": "midcap", "cagr_3y": 16.5},
    {"name": "ICICI Debt Fund", "category": "debt", "cagr_3y": 7.1}
  ],
  "projection": {"conservative": 250000, "expected": 320000, "optimistic": 400000},
  "rebalancing_plan": [
    {"phase": "Years 1-5", "equity": 50, "midcap": 30, "debt": 20},
    {"phase": "Years 6-10", "equity": 40, "midcap": 20, "debt": 40},
    {"phase": "Years 11-15", "equity": 25, "midcap": 10, "debt": 65}
  ]
}
```

**Crypto Recommendation Output**
```json
{
  "allocation": {"BTC": 45, "ETH": 30, "SOL": 15, "stablecoins": 10},
  "projection": {"conservative": -10, "expected": 25, "optimistic": 60},
  "risk_analysis": {"volatility": "high", "max_drawdown_1y": -35}
}
```

### 8. Non-Functional Requirements
- **Performance**: API responses returned within 2–3 seconds (with caching).
- **Reliability**: Graceful fallback to cached/sample data if external APIs fail.
- **Scalability**: Stateless backend services for easy horizontal scaling (post-hackathon consideration).
- **Security**: No storage of sensitive personal financial data; API keys stored securely in environment variables.
- **Usability**: Responsive design for desktop and mobile.

### 9. Development & Deployment Considerations
- Use environment variables for all API keys/configuration.
- Implement modular services so Mutual Fund and Crypto modules can be developed/tested independently.
- Provide a `.env.example` file and clear setup instructions for judges/evaluators to run locally.
