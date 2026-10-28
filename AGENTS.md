# Job — Agent Guidelines

## 1. Project Overview
Job is an automated job discovery, search filtering, and tracking application for the German labor market, integrating the official REST APIs of the Bundesagentur für Arbeit (`jobsuche.arbeitsagentur.de`).

---

## 2. Directory Layout
- `src/`:
  - `jobsuche_client.py`: Asynchronous API client for querying BA Jobsuche endpoints.
  - `job_tracker.py`: Local SQLite application pipeline and state manager.
- `requirements.txt`: Python dependencies (`httpx`, `pydantic`, `pytest`).
- `README.md`: Architecture and usage guide.

---

## 3. Development Commands
```bash
pip install -r requirements.txt
python -m py_compile src/jobsuche_client.py src/job_tracker.py
pytest tests/
```

---

## 4. Key Constraints & Data Privacy
1. **Never Commit SQLite Database:** `job_applications.db` and any personal CV or resume data must remain local and ignored by `.gitignore`.
2. **API Rate Limiting:** Apply polite request pacing when paginating through job postings.
3. **Branch Discipline:** Default target branch is `main`.
