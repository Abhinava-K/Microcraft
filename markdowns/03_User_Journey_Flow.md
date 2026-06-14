# User Journey Flow
## AI-Powered Investment Advisor Platform

### 1. Entry Point — Landing Page
- User arrives at the homepage.
- Sees a brief value proposition: "Get a personalized, AI-optimized investment portfolio — not generic advice."
- Two primary call-to-action options:
  - "Plan My Mutual Fund Portfolio"
  - "Optimize My Crypto Portfolio"
- Secondary option: "Ask the AI Advisor" (leads to advanced AI agent chat for either module).

---

### 2. Mutual Fund Module Journey

**Step 1 — Input Form**
- User selects "Plan My Mutual Fund Portfolio."
- Form fields:
  - Age (numeric input or slider)
  - Investment amount (numeric input, currency selector if needed)
  - Risk preference (Low / Medium / High — selectable cards or radio buttons)
  - Investment duration (slider or dropdown, in years)
- User clicks "Generate Portfolio."

**Step 2 — Processing State**
- Loading indicator while backend:
  - Fetches live fund data from MFAPI.
  - Runs allocation engine based on age, risk, and duration.
  - Computes top fund recommendations and projections.

**Step 3 — Results Dashboard**
- Displayed sections:
  1. **Recommended Allocation** — pie/donut chart showing percentage split (e.g., Equity 50%, Midcap 30%, Debt 20%).
  2. **Top 3 Recommended Funds** — cards/table with fund name, fund house, category, historical returns.
  3. **Expected Return Projection** — chart showing conservative/expected/optimistic growth over the investment duration.
  4. **Rebalancing Plan** — timeline/stepper visualization showing how allocation shifts across phases of the investment duration.
- User can adjust inputs and regenerate the portfolio at any time.

**Step 4 — Advanced Mode (Optional)**
- User clicks "Ask AI Advisor" within the Mutual Fund module.
- Chat interface opens; user types a query (e.g., "Suggest best SIP for 10 years under medium risk").
- AI agent responds with:
  - A brief natural language explanation.
  - A dynamically generated comparison table (fund names, categories, returns, risk levels).
- User can ask follow-up questions in the same chat session.

---

### 3. Crypto Module Journey

**Step 1 — Input Form**
- User selects "Optimize My Crypto Portfolio."
- Form fields:
  - Investment amount (numeric input)
  - Risk preference (Low / Medium / High)
- User clicks "Generate Portfolio."

**Step 2 — Processing State**
- Loading indicator while backend:
  - Fetches live market and historical data from CoinGecko.
  - Runs risk-adjusted allocation engine.
  - Computes return simulations and risk metrics.

**Step 3 — Results Dashboard**
- Displayed sections:
  1. **Recommended Allocation** — pie/donut chart (e.g., BTC 45%, ETH 30%, SOL 15%, Stablecoins 10%).
  2. **Expected Return Simulation** — chart showing best/average/worst case scenarios.
  3. **Risk Analysis** — summary panel showing volatility level, historical drawdown, and risk commentary.
- User can adjust inputs and regenerate the portfolio at any time.

**Step 4 — Advanced Mode (Optional)**
- User clicks "Ask AI Advisor" within the Crypto module.
- Chat interface opens; user types a query (e.g., "How should I invest ₹50,000 in crypto for high returns?").
- AI agent responds with:
  - A brief natural language explanation.
  - A live-data-backed recommendation table (asset, allocation %, rationale, risk level).
- User can ask follow-up questions in the same chat session.

---

### 4. Cross-Module Navigation
- Persistent navigation bar/header allows switching between Mutual Fund Module, Crypto Module, and AI Advisor at any point.
- Optional: a unified dashboard showing both portfolios side-by-side if a user has generated both.

---

### 5. End States
- **Successful recommendation generated**: User views results, can export/share (optional), or restart with new inputs.
- **API failure / fallback**: If live data is unavailable, user sees a notice ("Using cached/sample data") and still receives a complete recommendation.
- **AI agent query unclear**: Agent asks a clarifying follow-up question (e.g., "Could you specify your investment duration?") before generating a table.

---

### 6. Journey Summary Diagram (Textual)
```
Landing Page
   ├── Mutual Fund Module
   │      ├── Input Form (age, amount, risk, duration)
   │      ├── Processing (MFAPI calls + allocation engine)
   │      ├── Results Dashboard (allocation, top funds, projections, rebalancing plan)
   │      └── AI Advisor Chat (natural language queries → comparison tables)
   │
   └── Crypto Module
          ├── Input Form (amount, risk)
          ├── Processing (CoinGecko calls + allocation engine)
          ├── Results Dashboard (allocation, projections, risk analysis)
          └── AI Advisor Chat (natural language queries → recommendation tables)
```
