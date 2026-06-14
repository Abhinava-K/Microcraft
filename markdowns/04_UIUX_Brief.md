# UI/UX Brief
## AI-Powered Investment Advisor Platform

### 1. Design Vision
The interface should feel modern, trustworthy, and intelligent — conveying that the system "thinks" rather than just displays data. The visual language should balance financial professionalism (clean, data-forward) with a sense of approachability and personalization (friendly typography, clear guidance, conversational AI elements).

### 2. Design Principles
- **Clarity first**: Financial data (allocations, projections, risk) must be immediately understandable through charts and concise labels.
- **Personalization is visible**: The UI should visibly reflect that outputs change based on user inputs (e.g., show "Your Profile" summary alongside results).
- **Progressive disclosure**: Basic mode is simple and fast; Advanced AI mode is available but not forced on the user.
- **Trust through transparency**: Always show data sources (e.g., "Data from MFAPI", "Live prices via CoinGecko") and disclaimers.
- **Consistency across modules**: Mutual Fund and Crypto modules should share a common design system, differentiated by accent color or iconography.

### 3. Information Architecture

**Primary Navigation**
- Home / Landing
- Mutual Fund Advisor
- Crypto Advisor
- AI Chat Advisor (can be module-specific or global)
- About / How It Works (optional, explains methodology for credibility)

### 4. Key Screens & Layout Guidance

#### 4.1 Landing Page
- Hero section with headline (e.g., "Investment Advice That Thinks Before It Recommends") and subheadline explaining the personalization angle.
- Two prominent cards/buttons: "Mutual Fund Portfolio" and "Crypto Portfolio."
- Brief "How It Works" section (3-step visual: Enter Details → AI Analyzes Live Data → Get Personalized Plan).

#### 4.2 Mutual Fund Input Form
- Single-column form, vertically stacked for mobile-friendliness.
- Fields:
  - Age: slider with numeric display.
  - Investment amount: input field with currency symbol.
  - Risk preference: three selectable cards (Low, Medium, High) with short descriptive text and color coding (e.g., green/amber/red).
  - Duration: slider with year markers.
- Prominent "Generate My Portfolio" CTA button.

#### 4.3 Mutual Fund Results Dashboard
- Top section: "Your Profile" summary bar (age, amount, risk, duration) for context.
- Allocation visualization: donut chart with legend showing percentages and fund categories.
- Top 3 Funds: card layout, each showing fund name, fund house logo/name, category tag, historical return badge.
- Projection chart: line/area chart showing conservative/expected/optimistic growth curves over time.
- Rebalancing Plan: horizontal timeline/stepper showing allocation shifts across phases, with small donut or bar charts per phase.
- CTA: "Ask AI Advisor for more details" linking to chat mode.

#### 4.4 Crypto Input Form
- Simplified two-field form: Investment amount, Risk preference (same card style as mutual fund module but possibly with crypto-specific risk descriptions).
- "Generate My Crypto Portfolio" CTA button.

#### 4.5 Crypto Results Dashboard
- Allocation donut chart (BTC, ETH, SOL, Stablecoins, etc., with brand-recognizable color coding where appropriate, e.g., orange for BTC).
- Return simulation chart: best/average/worst case bands over a selected time horizon.
- Risk Analysis panel: volatility indicator (e.g., gauge or labeled badge: Low/Medium/High), historical drawdown stat, short explanatory text.
- CTA: "Ask AI Advisor for more details."

#### 4.6 AI Advisor Chat Interface
- Chat-style UI (message bubbles) similar to familiar chat assistants.
- Input box with placeholder examples (e.g., "Try: 'Suggest best SIP for 10 years under medium risk'").
- Agent responses render:
  - Short text explanation.
  - A formatted table (sortable if possible) for fund/crypto comparisons.
- Persistent disclaimer footer: "AI-generated suggestions are for educational purposes only."

### 5. Visual Style Guidance
- **Color palette**: Use a primary brand color (e.g., deep blue or teal for trust) with distinct accent colors for Mutual Fund vs. Crypto modules (e.g., blue family for Mutual Funds, purple/orange family for Crypto).
- **Typography**: Clean sans-serif fonts (e.g., Inter, Roboto) for readability of numerical data; slightly larger font sizes for key metrics (allocation %, returns).
- **Charts**: Use consistent chart styling (donut charts for allocation, line/area charts for projections, simple bar/gauge for risk).
- **Iconography**: Use simple line icons for risk levels, fund categories, and crypto assets to aid quick scanning.
- **Responsiveness**: Mobile-first layout for input forms; charts should resize/stack appropriately on smaller screens.

### 6. Interaction & Feedback Patterns
- Loading states should communicate what's happening (e.g., "Fetching live fund data...", "Analyzing market volatility...") rather than generic spinners, reinforcing the "thinking" narrative.
- Inline validation on form inputs (e.g., minimum investment amount, valid age range).
- Smooth transitions between input form and results dashboard (e.g., fade/slide) to maintain a polished feel.
- Hover/tap states on fund cards and chart segments to reveal additional details (tooltips).

### 7. Accessibility Considerations
- Sufficient color contrast for risk-level indicators and charts (don't rely on color alone — use labels/icons too).
- Keyboard-navigable forms and chat input.
- Readable font sizes (minimum 14px body text) and scalable chart text.

### 8. Trust & Transparency Elements
- Persistent small footer or badge: "Powered by live data from MFAPI & CoinGecko."
- Disclaimer visible on all results pages: "For educational/demo purposes only. Not financial advice."
- Optional "Why this recommendation?" expandable section explaining the logic behind allocations in plain language.
