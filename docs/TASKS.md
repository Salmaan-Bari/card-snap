# CardSnap First 10 Implementation Tasks

These tasks are intentionally very small and scoped to one Codex session each.

## 1) Create top-level app folders
- Create empty folders: `mobile/`, `backend/`, and `shared/`.
- Add `.gitkeep` in each new empty folder if needed.

## 2) Create backend app skeleton folders
- Inside `backend/`, create: `app/api`, `app/schemas`, `app/services`, `app/core`, `tests`.
- Do not add business logic yet.

## 3) Add backend entrypoint file
- Create `backend/app/main.py` with a minimal FastAPI app instance.
- Include a temporary root route (`GET /`) returning a simple JSON message.

## 4) Add backend dependencies file
- Create `backend/requirements.txt` with only foundational dependencies:
  - `fastapi`
  - `uvicorn`
  - `python-multipart`
- No AI or pricing SDKs yet.

## 5) Add backend health endpoint
- Add `GET /api/v1/health` route.
- Return status and version fields (hardcoded is fine for now).

## 6) Add analysis response schema
- Create `backend/app/schemas/analysis.py` with a `CardAnalysisResult` model.
- Include fields from `docs/APP_PLAN.md` section 7.

## 7) Add mock analysis service
- Create `backend/app/services/mock_analysis.py`.
- Implement one function that returns deterministic mock card output.

## 8) Add analyze-card API route
- Create `POST /api/v1/analyze-card` accepting multipart `image`.
- Call mock analysis service and return `CardAnalysisResult`.

## 9) Add mobile app skeleton folders
- Inside `mobile/`, create: `app/`, `src/components`, `src/services`, `src/types`, `src/utils`, `assets/`.
- Add placeholder `.gitkeep` files where useful.

## 10) Add mobile API client stub
- Create `mobile/src/services/api.ts` with a single exported function stub:
  - `analyzeCard(imageUri: string)`
- For now, return a local mocked object matching backend response shape.

---

Notes:
- Do **not** integrate real OpenAI or marketplace pricing APIs yet.
- Do **not** add auth/database yet.
- Keep each task small enough to complete, review, and commit independently.
