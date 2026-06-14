# Backend & Agent Implementation Plan
## Mapping to the Product Requirements (PRD & TRD)

Since the UI is handled by another team, our sole responsibility is to build the "brain" of the application. This plan outlines exactly how we will build the FastAPI backend, the allocation engines, and the LangGraph agents to fulfill the requirements from `01_PRD.md` and `02_Technical_Requirements_Document.md`.

---

### 1. Backend Architecture & Directory Structure

We will use Python with **FastAPI** because of its speed, asynchronous capabilities, and native compatibility with LangChain/LangGraph.

**Proposed Structure:**
```text
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point & CORS
│   ├── api/                    # Route handlers (Controllers)
│   │   ├── mf_routes.py        # /api/mf/...
│   │   ├── crypto_routes.py    # /api/crypto/...
│   │   └── agent_routes.py     # /api/agent/...
│   ├── core/                   # Mathematical Allocation Engines
│   │   ├── mf_engine.py        # Age/Risk/Duration matrix math
│   │   └── crypto_engine.py    # Volatility/Return math
│   ├── services/               # External API wrappers (MFAPI, CoinGecko)
│   │   ├── mfapi.py            # MFAPI fetch & calculate CAGR
│   │   └── coingecko.py        # CoinGecko fetch
│   └── agents/                 # LangGraph & LangChain implementation
│       ├── tools/              # Tools exposed to the LLM
│       ├── mf_agent.py         # Mutual Fund LangGraph state machine
│       └── crypto_agent.py     # Crypto LangGraph state machine
├── data/                       # Fallback JSON data (as required by PRD)
└── requirements.txt
```

---

### 2. Implementation Steps (The "How-To")

#### Phase 1: API Wrappers & Fallbacks (Fulfills TRD Section 6 & 9)
Before we can calculate anything, we need data.
1.  **MFAPI Service**: Build asynchronous functions to hit `api.mfapi.in`. Implement a TTL cache (using Python's `cachetools`). Create a fallback `sample_mf_data.json` so the app doesn't break during the demo if the API goes down.
2.  **CoinGecko Service**: Build asynchronous functions to fetch live crypto prices and historical data. Implement rate-limiting safeguards and a fallback `sample_crypto_data.json`.

#### Phase 2: Core Allocation Engines (Fulfills PRD Section 5.1 & 5.2)
This is the math behind the personalized recommendations.
1.  **Mutual Fund Engine (`mf_engine.py`)**: 
    *   Implement the Age-Risk matrix. Example: A 25-year-old with High risk gets `70% Equity, 20% Midcap, 10% Debt`.
    *   Implement the **Duration Rebalancing Formula** to shift percentages to debt as the investment matures.
2.  **Crypto Engine (`crypto_engine.py`)**:
    *   Implement the Risk matrix. Example: High risk allocates to Altcoins (SOL); Low risk focuses on BTC/Stablecoins.
    *   Calculate expected return projections using simple historical Monte Carlo or average-CAGR formulas.

#### Phase 3: The LangGraph Agents (Fulfills TRD Section 5)
This is where we implement the "Advanced Mode". We will use Google's **Gemini API** as the LLM core.
1.  **Define Tools**: We will wrap our `mf_engine` and `mfapi` functions into LangChain `@tool` decorators. Example: `@tool def get_historical_nav(scheme_code: str): ...`
2.  **Define the Graph (`mf_agent.py` & `crypto_agent.py`)**:
    *   Create a `State` definition that holds the chat history and user context.
    *   Create nodes: `AgentNode` (where Gemini decides what to do) and `ToolNode` (where the math/API calls are executed).
    *   Add edges conditional on tool calls.
3.  **System Prompts**: We must strictly prompt Gemini: *"You are an expert financial analyst. You must use the provided tools to fetch live data. Format your final response using Markdown tables. Add a disclaimer that this is not financial advice."*

#### Phase 4: API Routing & Frontend Integration
1.  **FastAPI Routes**: Expose `/api/mf/recommend`, `/api/crypto/recommend`, and `/api/agent/chat`.
2.  **CORS Config**: Allow `*` or the frontend's specific Vercel URL to prevent cross-origin errors when the UI team connects.

---

### 3. Open Questions for You Before We Code

> [!IMPORTANT]
> Please review and answer these before I initialize the backend repository.

1.  **Python Environment**: Should I create a standard `requirements.txt` / `venv`, or do you prefer `Poetry` for dependency management?
2.  **API Key**: I will need your Gemini API key shortly. Please make sure you have it ready (do not paste it yet).
3.  **Are we clear to initialize the `backend/` folder and start Phase 1?**
