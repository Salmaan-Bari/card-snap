# CardSnap App Plan (MVP-First)

## 1) Product Overview
CardSnap is a mobile app that helps users identify trading cards from a photo and estimate a current market value range.

For MVP, focus on **Pokémon cards** only to simplify recognition quality, pricing assumptions, and UX.

Primary user outcome:
- User uploads/takes a card photo
- App returns a likely match + estimated value range + confidence + notes

---

## 2) MVP Scope

### In scope
- React Native + Expo app with a simple 1-flow experience
- Photo input via camera or gallery
- Image preview before submit
- Backend API (FastAPI) to receive image and return mocked analysis response
- Deterministic mock card identification/pricing pipeline (no live integrations yet)
- Display result fields:
  - Card name
  - Set name
  - Condition estimate (basic)
  - Confidence score
  - Estimated value range
  - Notes

### Out of scope (for MVP)
- User accounts/auth
- Persistent card collection
- Real-time marketplace scraping
- Payments/checkout
- Social/community features

---

## 3) Non-MVP Features to Avoid for Now
Avoid these until MVP is stable:
- Multi-category card support (sports, Yu-Gi-Oh!, MTG)
- Complex grading simulation (PSA/BGS-like full grading)
- Portfolio tracking and P/L analytics
- Push notifications and price alerts
- OCR-heavy metadata extraction from tiny print
- Offline ML model on-device
- Admin dashboard

Reason: each adds complexity before core value (identify + estimate) is validated.

---

## 4) Recommended Repo Structure

```text
card-snap/
  mobile/                     # Expo React Native app
    app/                      # expo-router screens (or src/screens if preferred)
    src/
      components/
      services/
      types/
      utils/
    assets/
    .env.example

  backend/                    # FastAPI service
    app/
      api/
      core/
      models/
      schemas/
      services/
      main.py
    tests/
    .env.example
    requirements.txt (or pyproject.toml)

  docs/
    APP_PLAN.md
    API_CONTRACT.md           # optional later

  shared/                     # optional later for shared DTO/type contracts
```

Notes:
- Keep `mobile` and `backend` independent for simple local development.
- Add `shared/` only when contracts become hard to maintain manually.

---

## 5) Mobile App Screens

### A. Home / Capture Screen
- Actions:
  - “Take Photo”
  - “Upload from Gallery”
- Lightweight explanation of what CardSnap does

### B. Preview Screen
- Shows selected image
- Buttons:
  - Retake/Reselect
  - Analyze Card

### C. Loading/Analysis State
- Progress indicator + friendly copy (“Identifying card…”)
- Timeout/error fallback handling

### D. Result Screen
Display:
- Card Name
- Set
- Condition Estimate
- Confidence (e.g., 0–100%)
- Estimated Value Range (e.g., $12–$18)
- Notes (e.g., “Centering appears off; check corners manually.”)

Actions:
- Analyze another card
- (Later) Save result

### E. Error State (modal or screen)
- Could not analyze image
- Suggest retry with better lighting/background

---

## 6) Backend API Endpoints

Base path: `/api/v1`

### Health
- `GET /health`
- Response: service status/version

### Analyze Card (MVP core)
- `POST /analyze-card`
- Input:
  - multipart image upload (`image`)
  - optional metadata (platform, app version)
- Output (mocked for now):
  - `card_name`
  - `set_name`
  - `condition_estimate`
  - `confidence_score`
  - `estimated_value_min`
  - `estimated_value_max`
  - `currency`
  - `notes[]`
  - `source` (e.g., `mock_v1`)

### Future-safe (not implemented yet)
- `POST /pricing/refresh` (internal use)
- `GET /cards/{id}`

Keep the API contract stable even while internals are mocked.

---

## 7) Data Model / Schema Ideas

No DB required for MVP, but design response schemas now.

### `CardAnalysisResult` (response DTO)
- `request_id: str`
- `card_name: str`
- `set_name: str`
- `card_number: str | null`
- `condition_estimate: str` (e.g., Mint, Near Mint, LP)
- `confidence_score: float` (0–1)
- `estimated_value_min: float`
- `estimated_value_max: float`
- `currency: str` (default `USD`)
- `notes: list[str]`
- `pricing_source: str`
- `analyzed_at: datetime`

### Future DB tables (for Supabase/Postgres later)
- `users` (if auth added)
- `analysis_requests`
- `analysis_results`
- `card_reference`
- `pricing_snapshots`

---

## 8) AI + Pricing Pipeline (Practical MVP -> Scalable)

### MVP (mock-first)
1. Receive image
2. Basic image validation (format/size)
3. Return deterministic mock result (seeded by filename/hash so repeatable)
4. Log request ID + timing

### V1 (AI identify + mock pricing)
1. Send image to vision model
2. Extract likely card candidates
3. Pick top result + confidence
4. Return mock price range tied to card rarity tier

### V2 (AI + real pricing)
1. Identify card (name/set/number)
2. Normalize canonical card ID
3. Query pricing provider abstraction
4. Aggregate sold listing comps
5. Produce range + confidence + freshness timestamp

### Pricing abstraction pattern
- `PricingProvider` interface:
  - `get_price_range(card_identifier, condition) -> PriceRange`
- Implementations:
  - `MockPricingProvider`
  - `EbaySoldProvider` (later)

This avoids rewriting business logic when real pricing is introduced.

---

## 9) Security Rules for Public Repo

- Never commit real API keys or secrets
- Use `.env.example` only with placeholder names
- Add `.env` to `.gitignore` in both `mobile/` and `backend/`
- Validate upload size/type server-side
- Strip EXIF metadata where possible before long-term storage
- Avoid logging raw images or user-identifying payloads
- Add basic rate limiting on analyze endpoint
- CORS restricted to known app origins during web testing
- Keep dependency versions pinned/managed and run security checks in CI later

---

## 10) Development Phases (Codex-Friendly Small Tasks)

### Phase 0: Foundation
- Create repo folders (`mobile`, `backend`, `docs`)
- Add environment templates
- Add top-level README section for architecture

### Phase 1: Mobile UI skeleton
- Build capture, preview, loading, result screens
- Add local mocked result rendering
- Centralize API client module (even if mocked)

### Phase 2: Backend skeleton
- FastAPI app setup
- Health route + analyze route contract
- Pydantic schemas + mock analysis service

### Phase 3: Mobile ↔ Backend integration
- Wire image upload from mobile to backend
- Handle success/error states
- Add request timeout + retry UX

### Phase 4: Quality hardening
- Input validation, structured errors
- Basic tests for API contract
- Logging and request IDs

### Phase 5: AI/pricing upgrades (post-MVP)
- Swap mock identifier with AI model call
- Add pricing provider abstraction and first real data source

---

## 11) Exact Next 5 Implementation Tasks After Planning

1. **Scaffold project directories**
   - Create `mobile/`, `backend/`, and minimal starter files.

2. **Define API contract first**
   - Add `backend/app/schemas/analysis.py` with request/response models matching this plan.

3. **Create FastAPI MVP endpoint**
   - Implement `POST /api/v1/analyze-card` returning deterministic mock result.

4. **Create Expo screen flow (UI only)**
   - Build Capture → Preview → Loading → Result navigation with local mock JSON.

5. **Wire mobile upload to backend endpoint**
   - Replace local mock with real POST request; map backend response to Result screen.

---

This plan intentionally prioritizes shipping a usable MVP quickly while preserving a clean path to AI and real market pricing later.
