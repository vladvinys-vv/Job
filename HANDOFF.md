# Job — Project Handoff

## Current Status (October 2026)
- **Unified Location:** Standardized at `C:\Users\vladv\projects\Job`.
- **Default Branch:** `main` (clean, synchronized with `origin/main`).
- **Open-Source Integration:** Integrated `bundesAPI/jobsuche-api` patterns with async `httpx` client and local SQLite application tracker.
- **Hygiene & Standards:**
  - Standardized `.gitignore` protecting `.db` databases, caches, and environments.
  - Comprehensive `README.md`, `requirements.txt`, `AGENTS.md`, and this `HANDOFF.md`.

## Quick Start
```bash
pip install -r requirements.txt
python src/jobsuche_client.py
```

## Verification Commands
```bash
python -m py_compile src/jobsuche_client.py src/job_tracker.py
```
