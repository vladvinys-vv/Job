# Google Jules Rules for Job

## Role & Objectives
You are Google Jules assisting with **Job**, a German employment market and job opportunity search client integrating with the official Bundesagentur für Arbeit API and managing local application workflows via SQLite.

## Core Principles & Domain Standards
1. **Bundesagentur für Arbeit Integration:**
   - Adhere to the official Jobsuche API standards, query structures, and pagination parameters.
   - Maintain polite request cadence without triggering HTTP 429 rate limits.
2. **Local Application Lifecycle Tracking:**
   - Manage application statuses (`applied`, `interview`, `offer`, `rejected`) deterministically in local SQLite.
   - Ensure idempotent schema migrations and safe UTC timestamp formatting.
3. **Data Privacy & User Security:**
   - Never store private resume/CV files, cover letters, or personal applicant credentials in public git.
   - Local database files (`*.sqlite`, `*.db`) must remain excluded via `.gitignore`.
4. **Testing & Verification:**
   - All tests in `tests/` must pass (`pytest -v`).
