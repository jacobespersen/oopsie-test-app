# Oopsie Test App

Minimal Python app that triggers a fixable error and reports it to Oopsie(Work in progress) for testing the error-ingestion and fix pipeline.

## What it does

- **`app.py`** – Contains a deliberate, fixable bug: a function can return `None`, and the caller uses `.strip()` on the result, causing `AttributeError: 'NoneType' object has no attribute 'strip'`. The fix is a one-liner (e.g. add `or ""` or a None check).
- **`run.py`** – Entry point: runs the buggy code, catches the exception, and POSTs `error_class`, `message`, and `stack_trace` to your Oopsie instance at `POST /api/v1/errors`.

This gives you an end-to-end test: run the app → error is reported to Oopsie → (once the pipeline is built) worker can clone the repo, run Claude, and open a PR with the fix.

## How to run

1. **In Oopsie:** Create a project (e.g. via `POST /api/v1/projects`) and note the returned `api_key`. Optionally set `github_repo_url` and `github_token` for that project to this repo so the fix pipeline can clone and push later.

2. **In this project:**
   - Clone the repo (or use this folder).
   - Copy `.env.example` to `.env` and set your values:
     - `OOPSIE_API_URL` – Base URL of your Oopsie instance (default: `http://localhost:8000`).
     - `OOPSIE_API_KEY` – The project’s API key from Oopsie (required).
   - Install dependencies and run the trigger script:

   ```bash
   pip install -r requirements.txt
   cp .env.example .env   # then edit .env with your API key
   python run.py
   ```

   The app loads `OOPSIE_API_URL` and `OOPSIE_API_KEY` from the `.env` file (or from the environment if set there).

3. **Verify:** In Oopsie, confirm the error appears (e.g. in the DB or a future dashboard). Sending the same error multiple times is fine; Oopsie will upsert by fingerprint and increment occurrence count.

## Requirements

- Python 3.10+ (for `str | None` type hints; adjust if you need older support).
- Dependencies: `python-dotenv` (to load `.env`); install with `pip install -r requirements.txt`.
