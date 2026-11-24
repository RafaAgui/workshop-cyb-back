# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI Python backend for a cybersecurity workshop (`cyb-workshop-back`). It pairs with an Angular frontend running on `http://localhost:4201`. Auth uses JWT tokens (`python-jose`) with bcrypt password hashing (`passlib`/`bcrypt`).

## Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies from the pinned lockfile
pip install -r requirements.txt

# Run the development server
uvicorn main:app --reload

# Run on a specific port
uvicorn main:app --reload --port 8000
```

Dependencies are now pinned in `requirements.txt` (generated via `pip freeze`). After adding/upgrading a package in `venv`, refresh the lockfile:
```bash
pip freeze > requirements.txt
```

`bcrypt` is intentionally pinned to `4.0.1` — `bcrypt` 4.1+/5.x removed the `__about__` module that `passlib` 1.7.4 relies on to detect the backend version, which makes passlib mis-handle password truncation and raise `ValueError: password cannot be longer than 72 bytes` even for short passwords. Do not upgrade `bcrypt` past 4.0.x without also upgrading `passlib` (and re-testing `auth_service.py` hashing/verification).

## Architecture

The app follows a **feature-based module structure** rooted in `features/`, with cross-cutting concerns in `core/`:

- `main.py` — creates the FastAPI `app`, registers routers, and adds CORS middleware (origin: `http://localhost:4201`)
- `core/security.py` — JWT helpers shared across features: `create_access_token(data)` (signs with `SECRET_KEY`/`HS256`, 30 min expiry) and `verify_token(token)`. `SECRET_KEY` is hardcoded for the workshop; call out that it belongs in an env var before any real deployment.
- `core/dependencies.py` — `get_current_user`, a reusable FastAPI dependency that extracts the Bearer token via `HTTPBearer`, verifies it with `verify_token`, and returns the decoded payload (raises `401` if invalid/expired). Inject this into any endpoint that needs to require a valid JWT.
- `features/<domain>/` — each feature is a self-contained module:
  - `<domain>_router.py` — `APIRouter` with a URL prefix; imported and mounted in `main.py` via `include_router`
  - `<domain>_schemas.py` — Pydantic request/response models
  - `<domain>_service.py` — business logic (data access, hashing, verification), kept separate from the router

Current features:
- `features/auth/` — `/auth` prefix
  - `POST /auth/login` — validates credentials against `FAKE_USERS_DB` (in-memory stub in `auth_service.py`) via `verify_password` (passlib/bcrypt), then returns a signed JWT (`TokenResponse`)
  - `POST /auth/logout` — stub; backend is stateless, real logout happens client-side by discarding the token
- `features/protected/` — `/protected` prefix; example endpoints demonstrating `core/dependencies.get_current_user` (no `_schemas.py`/`_service.py`, just a router)
  - `GET /protected/me` — requires a valid JWT; returns `username`/`email` extracted from the token payload
  - `GET /protected/data` — requires a valid JWT; returns sample "secret" data for the authenticated user

When adding a new feature, create `features/<name>/<name>_router.py` (+ `_schemas.py` / `_service.py` as needed), define an `APIRouter` there, and `include_router` it in `main.py`. Put any auth/token logic shared across features in `core/`.

## Key Dependencies

| Package | Purpose |
|---|---|
| `fastapi` 0.135 | Web framework |
| `pydantic` v2 | Request/response models |
| `python-jose` | JWT encoding/decoding |
| `passlib` 1.7.4 + `bcrypt` 4.0.1 (pinned) | Password hashing — see version-pinning note above |
| `starlette` | ASGI foundation (comes with FastAPI) |
