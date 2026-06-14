# Frontend Development Guidelines
## AI-Powered Investment Advisor Platform

This document serves as a comprehensive guide for the frontend team on **what to build**, **how to build it**, and **how to correctly format request payloads** for our backend AI engine.

---

### 1. What to Build (Core UI Components)

Your primary objective is to create a premium, intuitive user interface that collects user data effortlessly and displays complex financial advice beautifully.

**Key Views to Implement:**
1.  **Investment Profiling Form:** A sleek, interactive form to collect user inputs (Age, Amount, Risk Appetite, Duration). 
2.  **Dynamic Loading State:** AI and external market APIs take time (5-10 seconds). You **must** build a dynamic loading screen with rotating text (e.g., "Fetching market data...", "Running simulations...", "Optimizing portfolio...") rather than a static spinner.
3.  **Financial Dashboard (Results View):** The centerpiece of the app. This will display the returned asset allocations, projected growth, and specific fund/crypto recommendations using beautiful charts and metric cards.
4.  **AI Advisor Chat Interface:** A conversational UI where users can ask follow-up questions. The AI's responses will include markdown tables and formatted text, so a robust markdown renderer is required.

---

### 2. How to Build It (Recommended Tooling)

To achieve the premium look and handle the complex data rendering, we highly recommend the following stack:

*   **Core Framework:** React (Next.js or Vite).
*   **Styling:** Tailwind CSS (for rapid, modern UI development).
*   **Graphing & Data Visualization:** 
    *   Use **[Recharts](https://recharts.org/)** or **[Tremor](https://www.tremor.so/)** to visualize the JSON responses.
    *   You will need to build **Donut/Pie Charts** for Asset Allocation (Equity vs. Debt vs. Midcap).
    *   You will need to build **Line/Area Charts** for Growth Projections (Conservative vs. Expected vs. Optimistic over time).
*   **Markdown Rendering (Crucial):**
    *   The AI Agent returns complex string data, including comparison tables.
    *   You **must** use `react-markdown` along with the `remark-gfm` plugin to properly render the agent's tables and text styling. Do not attempt to parse this manually.
*   **Error Handling:** Use toast notifications (e.g., `react-hot-toast`) to gracefully handle rate limit errors or timeouts.

---

### 3. Formatting the Request Body (Strict Input Constraints)

The backend has hardcoded validation rules to ensure the AI agent performs without hesitation. **You must enforce these constraints via UI elements** before sending the payload.

#### A. Mutual Fund Recommendations
**Target:** `POST /api/mf/recommend`

**Request Payload Format:**
```json
{
  "age": 28,
  "amount": 100000,
  "risk": "medium",
  "duration_years": 15
}
```

**Strict UI Constraints for this Payload:**
*   **`risk`**: Must be passed exactly as `"low"`, `"medium"`, or `"high"`. **Please use checkboxes or radio buttons** for this selection. Do not use a free-text input.
*   **`amount`**: Must be **>= 1000** and in **multiples of 100** (e.g., 1000, 1100). The backend will reject amounts like 1050.50. Use a number stepper with a `step="100"` attribute.
*   **`age`**: Must be **> 0**.
*   **`duration_years`**: Must be **> 0**.

*(Note: The backend will return a JSON object containing `allocation`, `top_funds`, `projection`, and `rebalancing_plan` for you to map to your charts).*

#### B. Crypto Recommendations
**Target:** `POST /api/crypto/recommend`

**Request Payload Format:**
```json
{
  "amount": 50000,
  "investment_horizon": "medium-term",
  "max_drawdown": 50
}
```

**Strict UI Constraints for this Payload:**
*   **`amount`**: Must be **>= 1000** and in **multiples of 100**.
*   **`investment_horizon`**: Must be exactly `"short-term"`, `"medium-term"`, or `"long-term"`. Use a select dropdown or radio buttons.
*   **`max_drawdown`**: Must be exactly `20`, `50`, or `80`. This represents the user's loss tolerance percentage. Use radio buttons or a discrete slider.

If the frontend sends invalid data, the backend will return a `422 Unprocessable Entity` error. Ensure all inputs are strictly controlled via the UI components.
