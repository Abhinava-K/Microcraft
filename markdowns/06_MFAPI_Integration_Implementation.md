# MFAPI Integration — Implementation Guide
## Mutual Fund Module Data Layer

### 1. Overview
MFAPI (https://www.mfapi.in) is a free, open API providing data for Indian mutual fund schemes — scheme metadata, historical NAV (Net Asset Value), and latest NAV. No authentication or API keys are required, and the production base URL is https://api.mfapi.in. This means there is **no key management needed** for this integration — only request handling, caching, and rate-limit-friendly design on our end.

> **Important note for the PRD/TRD**: References to an "MFAPI key" can be removed from setup docs — replace with "no auth required" so judges/developers don't waste time hunting for credentials.

---

### 2. Available Endpoints

- `GET /mf/search` — Search mutual fund schemes by name
- `GET /mf` — List all mutual fund schemes with pagination
- `GET /mf/{scheme_code}` — Get NAV history for a specific scheme
- `GET /mf/{scheme_code}/latest` — Get latest NAV for a specific scheme

Data is updated automatically with daily NAV refreshes, and responses are returned in JSON with standard HTTP status codes.

---

### 3. Example Requests

**Search for funds by AMC/keyword**
```
GET https://api.mfapi.in/mf/search?q=HDFC
```
Response:
```json
[
  { "schemeCode": 125497, "schemeName": "HDFC Top 100 Fund - Direct Plan - Growth" },
  { "schemeCode": 125498, "schemeName": "HDFC Top 100 Fund - Regular Plan - Growth" }
]
```

**Get NAV history (with optional date range)**
```
GET https://api.mfapi.in/mf/125497?startDate=2023-01-01&endDate=2023-12-31
```

**Get latest NAV for a scheme**
```
GET https://api.mfapi.in/mf/125497/latest
```
Response:
```json
{
  "meta": {
    "fund_house": "HDFC Mutual Fund",
    "scheme_type": "Open Ended Schemes",
    "scheme_category": "Equity Scheme - Large Cap Fund",
    "scheme_code": 125497,
    "scheme_name": "HDFC Top 100 Fund - Direct Plan - Growth",
    "isin_growth": "INF179K01BB2",
    "isin_div_reinvestment": null
  },
  "data": [
    { "date": "26-10-2024", "nav": "892.45600" }
  ],
  "status": "SUCCESS"
}
```

**List schemes with pagination**
```
GET https://api.mfapi.in/mf?limit=100&offset=0
```

---

### 4. Backend Service Design

Create a dedicated `mfapiService` module that wraps all calls, handles caching, and normalizes responses for the allocation engine.

#### 4.1 Folder structure (suggested)
```
/backend
  /services
    mfapiService.js
  /cache
    mfCache.js (in-memory or Redis wrapper)
  /routes
    mf.routes.js
```

#### 4.2 Service functions

```javascript
// services/mfapiService.js
const BASE_URL = "https://api.mfapi.in";

async function searchSchemes(query) {
  const res = await fetch(`${BASE_URL}/mf/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error("MFAPI search failed");
  return res.json();
}

async function getSchemeHistory(schemeCode, startDate, endDate) {
  let url = `${BASE_URL}/mf/${schemeCode}`;
  const params = new URLSearchParams();
  if (startDate) params.append("startDate", startDate);
  if (endDate) params.append("endDate", endDate);
  if (params.toString()) url += `?${params.toString()}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error(`MFAPI history fetch failed for scheme ${schemeCode}`);
  return res.json();
}

async function getLatestNav(schemeCode) {
  const res = await fetch(`${BASE_URL}/mf/${schemeCode}/latest`);
  if (!res.ok) throw new Error(`MFAPI latest NAV fetch failed for scheme ${schemeCode}`);
  return res.json();
}

async function listSchemes(limit = 100, offset = 0) {
  const res = await fetch(`${BASE_URL}/mf?limit=${limit}&offset=${offset}`);
  if (!res.ok) throw new Error("MFAPI scheme list fetch failed");
  return res.json();
}

module.exports = { searchSchemes, getSchemeHistory, getLatestNav, listSchemes };
```

---

### 5. Caching Layer

Since MFAPI has no auth but does implement rate limiting and recommends caching responses, wrap calls with a simple TTL cache.

```javascript
// cache/mfCache.js
const cache = new Map();
const TTL_MS = 30 * 60 * 1000; // 30 minutes

function getCached(key) {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() - entry.timestamp > TTL_MS) {
    cache.delete(key);
    return null;
  }
  return entry.data;
}

function setCached(key, data) {
  cache.set(key, { data, timestamp: Date.now() });
}

module.exports = { getCached, setCached };
```

```javascript
// example usage inside mfapiService.js
const { getCached, setCached } = require("../cache/mfCache");

async function getLatestNavCached(schemeCode) {
  const key = `latest:${schemeCode}`;
  const cached = getCached(key);
  if (cached) return cached;

  const data = await getLatestNav(schemeCode);
  setCached(key, data);
  return data;
}
```

For production/team builds, replace the in-memory `Map` with Redis using the same `get/set` interface.

---

### 6. Computing Historical Returns (CAGR) from NAV History

The allocation engine ranks funds by historical CAGR. Use NAV history to compute this:

```javascript
function calculateCAGR(navHistory, years) {
  // navHistory.data is sorted newest-first by default from MFAPI
  const sorted = [...navHistory.data].sort(
    (a, b) => parseDate(a.date) - parseDate(b.date)
  );

  const startNav = parseFloat(sorted[0].nav);
  const endNav = parseFloat(sorted[sorted.length - 1].nav);

  const cagr = (Math.pow(endNav / startNav, 1 / years) - 1) * 100;
  return Math.round(cagr * 100) / 100; // 2 decimal places
}

function parseDate(dateStr) {
  // MFAPI dates are in DD-MM-YYYY format
  const [day, month, year] = dateStr.split("-");
  return new Date(`${year}-${month}-${day}`);
}

module.exports = { calculateCAGR };
```

---

### 7. Backend Route Example

```javascript
// routes/mf.routes.js
const express = require("express");
const router = express.Router();
const mfapiService = require("../services/mfapiService");
const { calculateCAGR } = require("../utils/returns");

// GET top funds by category keyword (simplified — category mapping should be curated)
router.get("/funds", async (req, res) => {
  try {
    const { query } = req.query; // e.g., "HDFC Equity"
    const results = await mfapiService.searchSchemes(query);
    res.json(results.slice(0, 10)); // limit results
  } catch (err) {
    res.status(502).json({ error: "Failed to fetch fund data", details: err.message });
  }
});

// GET fund details + 3-year CAGR
router.get("/funds/:schemeCode/performance", async (req, res) => {
  try {
    const { schemeCode } = req.params;
    const today = new Date();
    const threeYearsAgo = new Date();
    threeYearsAgo.setFullYear(today.getFullYear() - 3);

    const history = await mfapiService.getSchemeHistory(
      schemeCode,
      threeYearsAgo.toISOString().split("T")[0],
      today.toISOString().split("T")[0]
    );

    const cagr3y = calculateCAGR(history, 3);
    res.json({ meta: history.meta, cagr_3y: cagr3y });
  } catch (err) {
    res.status(502).json({ error: "Failed to compute fund performance", details: err.message });
  }
});

module.exports = router;
```

---

### 8. Category Mapping (Curated List)

MFAPI does not provide a clean "category" filter for the allocation matrix (Equity / Midcap / Hybrid / Debt). Maintain a small curated mapping of scheme codes (or search keywords) per category for the demo, to ensure consistent and reliable recommendations:

```javascript
// config/fundCategoryMap.js
module.exports = {
  equity: [
    { schemeCode: 125497, name: "HDFC Top 100 Fund - Direct Plan - Growth" },
    // add 2-3 more for redundancy
  ],
  midcap: [
    // SBI Magnum Midcap, etc.
  ],
  hybrid: [
    // ICICI Balanced Advantage, etc.
  ],
  debt: [
    // SBI Magnum Gilt Fund, etc.
  ],
};
```

The allocation engine fetches `cagr_3y` for each scheme code in the relevant category and picks the top performer(s) to recommend.

---

### 9. Error Handling & Fallback Strategy

| Scenario | Handling |
|---|---|
| MFAPI request times out / fails | Return cached data if available; otherwise fall back to a local `sample_fund_data.json` with pre-fetched values |
| Scheme code invalid/not found | Skip and log; remove from category mapping candidates |
| NAV history too short for CAGR window | Use available shorter window and label as "since inception" |
| Rate limiting encountered | Increase cache TTL dynamically; queue/batch requests |

Sample fallback file structure:
```json
// data/sample_fund_data.json
{
  "125497": {
    "meta": { "fund_house": "HDFC Mutual Fund", "scheme_name": "HDFC Top 100 Fund - Direct Plan - Growth" },
    "cagr_3y": 14.2
  }
}
```

---

### 10. Summary Checklist
- [ ] No API key setup needed — confirm `.env` does not reference an MFAPI key.
- [ ] Implement `mfapiService` with search, history, latest NAV, and list functions.
- [ ] Add TTL-based caching (in-memory for hackathon, Redis-ready for scale).
- [ ] Implement CAGR calculation utility from NAV history.
- [ ] Curate a category-to-scheme-code mapping for Equity/Midcap/Hybrid/Debt.
- [ ] Add fallback sample data for offline/demo resilience.
- [ ] Expose `/api/mf/funds` and `/api/mf/funds/:schemeCode/performance` (or equivalent) for the allocation engine and AI agent tools to consume.
