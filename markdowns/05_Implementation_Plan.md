# Implementation Plan
## AI-Powered Investment Advisor Platform (Hackathon Build)

### 1. Overall Strategy
Given hackathon time constraints, the build is split into phases prioritizing a working end-to-end demo first (core flows for both modules with basic allocation logic and real API data), followed by enhancements (AI agent, rebalancing visualizations, refined UI).

---

### 2. Phase 1 — Foundation & Setup
**Goals**: Project scaffolding, API access, basic UI shell.

Tasks:
- Set up frontend project (React/Next.js) with routing for Landing, Mutual Fund, Crypto, and AI Chat pages.
- Set up backend project (Node/Express or Python/FastAPI) with basic API structure.
- Obtain/test access to MFAPI and CoinGecko endpoints; verify sample responses.
- Set up environment variable configuration for any required API keys (CoinGecko free tier may not require a key; Claude API key required for AI agent).
- Establish shared design tokens (colors, fonts, spacing) per UI/UX Brief.

---

### 3. Phase 2 — Mutual Fund Module (Core)
**Goals**: Functional input-to-output flow with real data.

Tasks:
- Build Mutual Fund input form (age, amount, risk, duration) with validation.
- Define allocation matrix (age bands × risk levels × duration bands → asset class %).
- Implement backend endpoint `/api/mf/recommend`:
  - Accepts user inputs.
  - Computes target allocation via matrix.
  - Fetches fund lists/NAV history from MFAPI for relevant categories.
  - Ranks funds by historical CAGR; selects top fund per category.
  - Computes simple return projections (conservative/expected/optimistic).
- Implement rebalancing logic: split duration into phases, recompute allocation per phase using adjusted age.
- Build Results Dashboard UI:
  - Allocation donut chart.
  - Top 3 funds cards.
  - Projection chart.
  - Rebalancing timeline.
- Add caching for MFAPI responses to handle repeated requests efficiently.

---

### 4. Phase 3 — Crypto Module (Core)
**Goals**: Functional input-to-output flow with real data.

Tasks:
- Build Crypto input form (amount, risk).
- Define risk-based allocation templates (Low/Medium/High → BTC/ETH/SOL/Stablecoin weights).
- Implement backend endpoint `/api/crypto/recommend`:
  - Fetches current and historical price data from CoinGecko for selected assets.
  - Computes volatility and historical return metrics.
  - Adjusts/validates allocation weights based on risk profile and volatility data.
  - Runs simple return simulation (best/average/worst case based on historical returns).
- Build Results Dashboard UI:
  - Allocation donut chart.
  - Return simulation chart.
  - Risk analysis panel.
- Add caching for CoinGecko responses to manage rate limits.

---

### 5. Phase 4 — AI Agent (Advanced Mode)
**Goals**: Natural language query support for both modules.

Tasks:
- Design system prompt for the AI agent, defining its role, available tools, output format (markdown table + brief explanation), and disclaimers.
- Implement backend tool functions callable by the agent:
  - `get_mutual_fund_data(category, filters)` — wraps MFAPI calls.
  - `get_crypto_market_data(coins, timeframe)` — wraps CoinGecko calls.
  - `compute_allocation(profile)` — reuses Phase 2/3 allocation logic.
  - `compute_projection(portfolio, duration)` — reuses projection/simulation logic.
- Implement backend endpoints `/api/mf/agent` and `/api/crypto/agent` (or a unified `/api/agent` with module context) that pass user queries + tool definitions to the Claude API.
- Build Chat UI:
  - Message thread with user/agent bubbles.
  - Render agent's markdown tables as formatted tables in the UI.
  - Input box with example query suggestions.
- Test with representative queries:
  - "Suggest best SIP for 10 years under medium risk."
  - "How should I invest ₹50,000 in crypto for high returns?"

---

### 6. Phase 5 — Polish & Demo Readiness
**Goals**: Ensure reliability, visual polish, and a compelling demo narrative.

Tasks:
- Add fallback/sample data for both modules in case live APIs fail during the demo.
- Refine loading states with descriptive messages ("Analyzing live fund data...", etc.).
- Add "Your Profile" summary and "Why this recommendation?" explanatory sections for transparency.
- Cross-browser/responsive testing (desktop + mobile).
- Add disclaimers and data-source attributions throughout.
- Prepare a demo script highlighting:
  - Different outputs for different age/risk/duration combinations (mutual funds).
  - Different outputs for different risk levels (crypto).
  - Live AI agent responses to natural language queries.

---

### 7. Suggested Timeline (Example for a 24–48 Hour Hackathon)

| Time Block | Focus |
|---|---|
| Hours 0–4 | Phase 1: Setup, API verification, design tokens |
| Hours 4–12 | Phase 2: Mutual Fund module (form, allocation logic, dashboard) |
| Hours 12–18 | Phase 3: Crypto module (form, allocation logic, dashboard) |
| Hours 18–28 | Phase 4: AI agent integration and chat UI |
| Hours 28–36 | Phase 5: Polish, fallback handling, responsive fixes |
| Hours 36–44 | Testing, demo script preparation, rehearsal |
| Remaining time | Buffer for bug fixes and final touches |

*(Adjust proportionally for shorter or longer hackathon durations.)*

---

### 8. Team Role Suggestions (if applicable)
- **Frontend Developer(s)**: Build UI components, charts, chat interface, responsive layouts.
- **Backend Developer(s)**: Build API endpoints, allocation engines, caching, AI agent tool integration.
- **Data/Logic Owner**: Define and refine allocation matrices, projection formulas, and risk models.
- **Designer (or shared role)**: Ensure visual consistency per UI/UX Brief, create chart styling and color system.
- **Presenter/Storyteller**: Prepare demo narrative emphasizing personalization and "thinking before recommending" angle.

---

### 9. Key Risks & Contingencies
| Risk | Contingency |
|---|---|
| API downtime during demo | Pre-cache sample responses for known demo inputs |
| AI agent latency | Pre-test common queries; consider showing a "typing/analyzing" animation to mask latency |
| Allocation logic complexity underestimated | Start with a simple lookup-table-based matrix; only add statistical optimization if time permits |
| Time overrun on AI agent integration | Treat AI agent as a stretch goal after both core dashboards are functional |
