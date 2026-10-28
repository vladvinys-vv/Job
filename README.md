# Job (German Job Search & Application Tracker)

Asynchronous Python client and local application tracker for German employment listings, integrating the official REST APIs of the **Bundesagentur für Arbeit** (`jobsuche.arbeitsagentur.de`) inspired by [`bundesAPI/jobsuche-api`](https://github.com/bundesAPI/jobsuche-api).

---

## 1. Key Capabilities
- **Direct Access to Bundesagentur für Arbeit:** Query official German job listings by keyword, location, PLZ, and commuting radius (`Umkreis`).
- **Employment Filtering:** Filter by `Vollzeit`, `Teilzeit`, `Minijob`, and vocational training (`Ausbildung`).
- **Application Tracking:** Local SQLite database (`job_applications.db`) for tracking application milestones (`FOUND`, `APPLIED`, `INTERVIEW`, `OFFER`, `REJECTED`).
- **Cross-Project Synergy:** Seamlessly integrates with [BueroHelfer](https://github.com/vladvinys-vv/BueroHelfer) and [German-Company-Scraper](https://github.com/vladvinys-vv/German-Company-Scraper).

---

## 2. Quick Start

### Installation
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Search Jobs Example
```python
import asyncio
from src.jobsuche_client import JobsucheClient
from src.job_tracker import JobTrackerDB

async def main():
    client = JobsucheClient()
    tracker = JobTrackerDB()

    # Search for software developer roles in Hamburg within 25 km
    jobs = await client.search_jobs("Softwareentwickler", location="Hamburg", radius_km=25)
    print(f"Found {len(jobs)} postings.")

    for job in jobs[:5]:
        print(f"- {job.title} at {job.employer} ({job.city})")
        tracker.add_job(job.job_id, job.title, job.employer, job.city)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Architecture & Guidelines
For detailed agent directives and maintenance standards, see [AGENTS.md](AGENTS.md) and [HANDOFF.md](HANDOFF.md).
