# Project: DB-Scout by Team ZeroKelvin

**Objective:** Transition the frontend from mock data (Express server) to the LIVE FastAPI backend, and implement the new "Schema Selection" flow.

---

## Current Context & Problem

Currently, the Vite frontend is hitting a mock Express server (`server.ts`) running on port 3000, which returns dummy `setTimeout` responses.

We now have a **LIVE FastAPI backend** running (default: `http://localhost:8000`). A new endpoint has been added to the FastAPI backend: `GET /database/schemas` which returns a list of schemas from the connected database.

---

## Task 1: The Great API Migration (Kill the Mocks)

### 1.1 Bypass `server.ts`
Update the frontend API configuration to point directly to the live FastAPI backend at `http://localhost:8000` instead of the local mock server.

**Action Items:**
- Update `src/config.ts` or `vite.config.ts` proxy configuration
- Point all API calls to `http://localhost:8000`
- Keep `server.ts` for reference but stop using it in development

### 1.2 Audit All Fetch Calls
Search the entire `src/` directory for:
- Hardcoded API responses
- Dummy JSON arrays
- Dummy markdown text
- Mock setTimeout patterns

**Focus Areas:**
- Zustand stores (`src/store.ts`)
- API utility files
- Component `useEffect` hooks
- Gateway and Scouting components

### 1.3 Endpoint Mapping
Ensure the frontend calls these EXACT FastAPI endpoints:

| Endpoint | Method | Payload | Purpose |
|----------|--------|---------|---------|
| `/database/test` | POST | `{ config }` | Test database connection |
| `/database/schemas` | GET | None (uses active DB connection) | **NEW** - Retrieve list of schemas |
| `/analysis/run` | POST | `{ user_id, schema_name }` | Run scout analysis (schema_name can be array or string) |
| `/chat` | POST | `{ query, rag_corpus_id, session_id }` | Chat with the scout agent |

---

## Task 2: Implement the New "Schema Selection" Flow

The `Gateway` (Onboarding) screen must accommodate the new `/database/schemas` endpoint.

### New UI Flow for the Gateway

**Step 1: Connection**
- User enters DB credentials
- Click "Test Connection" → `POST /database/test`

**Step 2: Schema Reconnaissance (NEW)**
- If connection successful → automatically call `GET /database/schemas`
- Show loading state while fetching

**Step 3: Selection UI**
- Display retrieved schemas as selectable checkboxes or multi-select dropdown
- Allow user to select one or more schemas

**Step 4: Deployment**
- "Deploy Scout Agent" button only active if at least one schema is selected
- On click → trigger loading animation
- Call `POST /analysis/run` with selected schema(s)

---

## Task 3: Hook up the Real Data Processors

Find where the frontend renders AI data and ensure it uses real GCP/Vertex output from Zustand global state.

### 3.1 Intelligence Docs (`DataDictionary.tsx`)
- Fetch markdown file using `md_gcs_path` from backend
- Implement backend proxy if GCS paths are private: `GET /api/download?path=...`
- Remove hardcoded Lorem Ipsum markdown

### 3.2 Command Center Sidebar
- Dynamically map over `preview_tables` array from `POST /analysis/run`
- Replace hardcoded table lists

### 3.3 ERD Mapper & Data Vitals
- Comment out dummy Mermaid nodes/edges
- Comment out dummy Recharts data
- Set up fetch call for `json_gcs_path` file download and parsing

---

## Execution Strategy

**Phase 1: API Configuration & State Management**
1. Create/update `src/config.ts` with FastAPI base URL
2. Update global Zustand store to accept real API responses
3. Create API utility functions for all endpoints

**Phase 2: Gateway Component Overhaul**
1. Add Schema Selection UI component
2. Implement new flow logic (Connection → Reconnaissance → Selection → Deployment)
3. Wire up `GET /database/schemas` call

**Phase 3: Data Integration**
1. Update DataDictionary, Sidebar, ERD components
2. Rip out dummy data
3. Wire up GCS file fetching

---

## 🎯 Complete Mock API & Data Inventory

### Location 1: `server.ts` - Express Server (DEPRECATED)
**Status:** Remove or archive this file entirely
**Mock Endpoints:**
- `POST /api/database/test` (Lines 12-18)
  - Mock: Returns success after `1500ms setTimeout`
  - Real: Should match FastAPI `POST /database/test`
  
- `GET /api/database/schemas` (Lines 20-30)
  - Mock: Returns hardcoded array `["public", "bikestore", "olist", "pg_toast"]`
  - Real: Should call `GET /database/schemas` from FastAPI
  
- `POST /api/analysis/run` (Lines 32-51)
  - Mock: Returns dummy GCS paths and fake table names
  - Real: Should match FastAPI `/analysis/run` response
  
- `POST /api/chat` (Lines 53-66)
  - Mock: Returns hardcoded markdown response after `2000ms setTimeout`
  - Real: Should match FastAPI `/chat` response

---

### Location 2: `src/components/IntelligenceDocs.tsx` - Dummy Markdown Content
**Status:** Wire up to real `mdGcsPath`
**Lines:** 45-68 contain mock markdown data
**Mock Data:**
```
const mockMarkdown = `
# Database Intelligence Report
[Lorem ipsum placeholder content]
...
`;
```
**Mitigation:**
- Replace `setTimeout` with fetch call using `mdGcsPath` from store
- Implement GCS proxy if paths are private: `GET /api/download?path=...`
- Handle markdown parsing from actual backend response

---

### Location 3: `src/components/ERDMapper.tsx` - Hardcoded Mermaid Diagram
**Status:** Wire up to real `jsonGcsPath`
**Lines:** 33-54 contain dummy ER diagram definition
**Mock Data:**
```javascript
const definition = `
  erDiagram
    USERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    ...
`;
```
**Mitigation:**
- Fetch actual entity relationships from `jsonGcsPath`
- Parse JSON and dynamically generate Mermaid definition
- Implement error handling for malformed GCS data
- Replace `setTimeout(2000)`  with actual fetch call

---

### Location 4: `src/components/DataVitals.tsx` - Hardcoded Chart Data
**Status:** Wire up to real metrics from `jsonGcsPath`
**Lines:** 22-41 contain mock Recharts data arrays
**Mock Data:**
```javascript
const rowData = [
  { name: 'Users', count: 12450 },
  { name: 'Orders', count: 84200 },
  // ... etc
];

const anomalyData = [
  { time: '00:00', value: 12 },
  // ... etc
];
```
**Mitigation:**
- Extract real table statistics from the JSON file returned by `/analysis/run`
- Fetch metrics dynamically from `jsonGcsPath`
- Remove hardcoded static data
- Replace `setTimeout(1500)` loading state with actual fetch logic

---

### Location 5: `src/Gateway.tsx` - API Endpoint Structure
**Status:** Partially updated, needs API base URL configuration
**Lines:** 42-75 contain fetch calls to `/api/database/test` and `/api/database/schemas`
**Current:** Points to mock `server.ts` on `:3000`
**Mitigation:**
- Update `fetch('/api/database/test')` to use FastAPI base URL (e.g., `http://localhost:8000/database/test`)
- Update `fetch('/api/database/schemas')` to use FastAPI
- Create `src/config.ts` with configurable API base URL (currently hardcoded as relative `/api/`)

---

### Location 6: `src/components/ScoutChat.tsx` - Chat API Calls
**Status:** Hardcoded `/api/chat` endpoint
**Lines:** 46-56 contain fetch call to chat endpoint
**Current:** Points to mock server
**Mitigation:**
- Update endpoint to use FastAPI base URL
- Ensure payload matches: `{ query, rag_corpus_id, session_id }`
- Connect real responses to message display

---

### Location 7: `src/Scouting.tsx` - Analysis Run Call
**Status:** Hardcoded `/api/analysis/run` endpoint
**Lines:** 23-28 contain fetch call to analysis endpoint
**Current:** Points to mock server with `setTimeout` animations
**Mitigation:**
- Update endpoint URL to FastAPI
- Ensure payload matches: `{ user_id, schema_name }`
- Handle real API response timing (may take longer than 8s)
- Keep loading state animations but tie to real API response

---

### Location 8: `vite.config.ts` - No Proxy Configuration
**Status:** Missing proxy for API requests
**Current:** No dev server proxy setup
**Mitigation:**
- Add Vite proxy configuration to forward `/api/*` requests to FastAPI
- Example:
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```
OR update all fetch calls to use `http://localhost:8000/database/...` directly

---

## 📋 Migration Checklist

### Phase 1: API Configuration
- [ ] Create `src/config.ts` with `API_BASE_URL` export
- [ ] Update `vite.config.ts` to include dev proxy OR update all fetch URLs
- [ ] Remove `server.ts` references from docs and deployment scripts
- [ ] Update package.json scripts to stop running `npm run dev` (Express server)

### Phase 2: Gateway Component
- [ ] Update fetch URLs in `src/Gateway.tsx` to use new API base
- [ ] Test connection flow with real FastAPI
- [ ] Verify schemas endpoint returns correct data
- [ ] Test schema selection UI/UX

### Phase 3: Component Integration
- [ ] `IntelligenceDocs.tsx`: Wire up `mdGcsPath` fetch
- [ ] `ERDMapper.tsx`: Wire up `jsonGcsPath` fetch
- [ ] `DataVitals.tsx`: Wire up metrics from JSON
- [ ] `ScoutChat.tsx`: Update endpoint URL
- [ ] `Scouting.tsx`: Update endpoint URL

### Phase 4: Testing & Cleanup
- [ ] Test all components with real FastAPI responses
- [ ] Verify error handling for network failures
- [ ] Remove all hardcoded mock data comments
- [ ] Archive `server.ts` for reference

---

## Code Changes Required (Priority Order)

See the attached code files for:
- `src/config.ts` - API configuration (NEW)
- `src/api/client.ts` - HTTP client utilities (NEW)
- `src/store.ts` - Updated Zustand state
- `src/Gateway.tsx` - Schema Selection flow with real API
- `src/components/IntelligenceDocs.tsx` - Real markdown fetch
- `src/components/ERDMapper.tsx` - Real diagram data
- `src/components/DataVitals.tsx` - Real chart data
- `src/components/ScoutChat.tsx` - Real chat endpoint
- `src/Scouting.tsx` - Real analysis endpoint
- `vite.config.ts` - Updated proxy configuration
