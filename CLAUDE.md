# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is QuickT

Online bus ticket purchasing platform for Togo. Users can search routes, buy tickets online with mobile money (Flooz/T-Money), receive digital tickets with QR codes, plan trips, and interact with bus agencies. Agencies manage their buses, schedules, and departures through a dedicated dashboard.

## Commands

### Backend (run from `backend/`)
```bash
make dev                    # uvicorn on :8095 with --reload
make test                   # migrate test DB + pytest -v
make reset-with-fixtures    # drop + create + migrate + seed demo data
make setup                  # first-time: install + create DB + migrate
make migrate-up             # apply pending SQL migrations
make migrate-down           # rollback last migration
make migrate-status         # show applied/pending migrations
```

Run a single test file or test:
```bash
cd backend
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/quickt_db_test" uv run pytest tests/domains/test_auth.py -v
```

Lint:
```bash
cd backend && uv run ruff check .
```

### Frontend (run from `frontend/`)
```bash
npm start          # vite dev server on :3001 (proxies /api + /uploads to :8095)
npm test           # vitest run
npm run test:watch # vitest in watch mode
npm run build      # production build
```

### Docker (from project root)
```bash
docker compose up --build   # backend :8095, frontend :80, postgres
```

## Architecture

### Backend

FastAPI + async SQLAlchemy + PostgreSQL (asyncpg). Python 3.13+, managed with `uv`.

**Domain structure** — each domain in `app/domains/<name>/` has four files:
- `models.py` — SQLAlchemy ORM models
- `schemas.py` — Pydantic request/response schemas
- `service.py` — business logic as a class taking `AsyncSession` in constructor
- `router.py` — FastAPI router, injects dependencies, delegates to service

All API routes are under `/api/v1/<domain>`. Swagger docs at `/api/docs`.

**Core modules** (`app/core/`):
- `security.py` — JWT creation/verification, bcrypt password hashing, ticket/booking code generation
- `exceptions.py` — HTTP exception subclasses with unified JSON error handler
- `storage.py` — file upload abstraction (local or S3)
- `mobile_money.py` — mobile money payment integration (Flooz/T-Money via Paygate/CinetPay)
- `email.py` — email sending via AWS SES
- `qr.py` — QR code generation for digital tickets

**Auth** — JWT access + refresh tokens. Dependencies in `app/dependencies.py`: `get_current_user`, `require_admin`, `require_agency_staff`, `require_agency_staff_or_admin`.

**User roles**: `customer`, `agency_staff`, `admin`.

**Database session** — `app/database.py` provides `get_db()` async generator. Session auto-commits on success, rolls back on exception.

**Migrations** — raw SQL files in `backend/migrations/`, NOT Alembic. Naming: `NNN_up_<name>.sql` / `NNN_down_<name>.sql`. Runner: `scripts/migrate.py`. Tracked in `schema_migrations` table.

**Fixtures** — JSON seed data in `backend/data/`, loaded by `scripts/seed_db.py`.

### Frontend

React 19 + Vite + TanStack Query v5 + Tailwind CSS 3. PWA-enabled via vite-plugin-pwa.

**Data flow pattern**: `services/<domain>.service.jsx` -> `hooks/use<Domain>.jsx` -> components/pages

**Auth**: `context/AuthContext.jsx` provides `useAuth()` hook. Token refresh handled by axios interceptor.

**Routing**: two shells in `App.jsx`:
- `<Layout />` — landing pages with Navbar + Footer
- `<AppLayout />` — authenticated app with mobile-first bottom nav
- `<RequireAuth roles={[...]}>` wraps role-gated routes

**i18n**: custom `t()` helper. Default locale: French.

## Key Conventions

- All SQLAlchemy relationships must use explicit `selectinload()` in service queries
- Backend port: **8095**
- Frontend dev port: **3001**
- Ruff config: `target-version = "py313"`, `line-length = 100`
- Tests use per-test isolated databases cloned from a template DB
- `pytest-asyncio` with `asyncio_mode = "auto"`
- Currency: XOF (FCFA)
- Design: Deep Blue (#1e40af) primary + Warm Orange (#f97316) accent

## Demo Accounts

| Email | Password | Role |
|-------|----------|------|
| `customer@quickt.tg` | `password123` | Customer |
| `agency@quickt.tg` | `password123` | Agency Staff (STIF Transport) |
| `admin@quickt.tg` | `password123` | Platform Admin |
