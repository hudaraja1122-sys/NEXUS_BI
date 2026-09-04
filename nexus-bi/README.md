# NEXUS BI — Phase 1 Skeleton

Autonomous AI Business Intelligence Analyst. **This is the Phase 1
foundation only** (monorepo structure, Next.js frontend, FastAPI backend,
env config, CORS, health endpoint, design tokens) — per the build order in
the master spec, later phases (dataset ingestion, DuckDB analytics, Gemini
+ LangGraph agent, visualizations, PDF reports, polish) are built on top of
this incrementally, not all at once.

## Structure

```
nexus-bi/
├── frontend/          # Next.js 15 + TypeScript + Tailwind
│   ├── app/           # App router: layout.tsx, page.tsx, globals.css
│   ├── components/ui/ # shadcn-style primitives land here (Phase 6+)
│   └── lib/           # api.ts (backend client), types.ts (Phase 2+)
└── backend/           # FastAPI + Pydantic
    ├── app/
    │   ├── main.py         # app factory, CORS, /health
    │   ├── core/config.py  # typed settings, all env vars
    │   ├── services/       # llm_provider.py (Gemini abstraction stub)
    │   └── api/             # routers land here (Phase 2+)
    └── data/            # local uploads/, reports/, nexus.duckdb
```

## Run locally

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in GEMINI_API_KEY when you reach Phase 4
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/health` — should return `{"status": "ok", ...}`.
Interactive schema at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Visit `http://localhost:3000`.

## Environment variables

See `backend/.env.example` and `frontend/.env.local.example`. The model
name (`GEMINI_MODEL`) and agent limits (`MAX_INVESTIGATION_STEPS`,
`MAX_LLM_CALLS_PER_QUESTION`) are config-driven — never hardcoded in code,
per spec sections 3–4.

## Next steps (Phase 2 — Dataset)

- CSV/XLSX upload endpoint + validation
- Pandas-based profiling (schema, types, nulls, cardinality)
- Data-quality score
- Dataset page in the frontend

## Status

Phase 1 only. No arbitrary code execution exists anywhere in this codebase
(and per the spec, never will — Gemini only returns structured JSON that
deterministic Python/DuckDB tools act on).
