"""
German Jobsuche API Client
Interfaces with the German Federal Employment Agency (Bundesagentur für Arbeit) API,
incorporating open data patterns from bundesAPI/jobsuche-api and bund.dev.
"""

from __future__ import annotations
import asyncio
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import httpx


@dataclass
class JobPosting:
    job_id: str
    title: str
    employer: str
    city: str
    postal_code: Optional[str] = None
    employment_type: Optional[str] = "Vollzeit"  # Vollzeit, Teilzeit, Minijob, etc.
    published_date: Optional[str] = None
    application_url: Optional[str] = None
    description: Optional[str] = None


class JobsucheClient:
    """
    Asynchronous client for Bundesagentur für Arbeit Jobsuche API.
    Public API: https://rest.arbeitsagentur.de/infosysbub/jobboerse/pc/v4/jobs
    """

    BASE_URL: str = "https://rest.arbeitsagentur.de/infosysbub/jobboerse/pc/v4/jobs"
    # Standard public client key used by Bundesagentur für Arbeit web frontend
    DEFAULT_API_KEY: str = "jobboerse-2f7653f3-0f16-4546-b1a6-0d4d4d5554f8"

    def __init__(self, api_key: Optional[str] = None, timeout: float = 15.0):
        self.api_key = api_key or self.DEFAULT_API_KEY
        self.timeout = timeout
        self.headers = {
            "X-API-Key": self.api_key,
            "User-Agent": "JobsucheAgent/1.0 (+https://github.com/vladvinys-vv/Job)",
            "Accept": "application/json",
        }

    async def search_jobs(
        self,
        keywords: str,
        location: Optional[str] = None,
        radius_km: int = 25,
        page: int = 1,
        page_size: int = 20,
    ) -> List[JobPosting]:
        """
        Search active job postings in Germany by keyword and location.
        """
        params: Dict[str, Any] = {
            "was": keywords,
            "page": page,
            "size": page_size,
        }
        if location:
            params["wo"] = location
            params["umkreis"] = radius_km

        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            try:
                response = await client.get(self.BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    jobs: List[JobPosting] = []
                    for item in data.get("stellenangebote", []):
                        jobs.append(
                            JobPosting(
                                job_id=item.get("refnr", ""),
                                title=item.get("titel", item.get("beruf", "")),
                                employer=item.get("arbeitgeber", ""),
                                city=item.get("arbeitsort", {}).get("ort", ""),
                                postal_code=item.get("arbeitsort", {}).get("plz"),
                                published_date=item.get("aktuelleVeroeffentlichungsdatum"),
                                employment_type=item.get("arbeitszeit", "Vollzeit"),
                            )
                        )
                    return jobs
            except httpx.HTTPError:
                pass
        return []

    async def get_job_details(self, job_ref: str) -> Optional[JobPosting]:
        """
        Fetch full details for a single job reference number.
        """
        endpoint = f"https://rest.arbeitsagentur.de/infosysbub/jobboerse/pc/v2/jobdetails/{job_ref}"
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            try:
                response = await client.get(endpoint)
                if response.status_code == 200:
                    data = response.json()
                    return JobPosting(
                        job_id=job_ref,
                        title=data.get("titel", ""),
                        employer=data.get("arbeitgeber", ""),
                        city=data.get("arbeitsort", {}).get("ort", ""),
                        postal_code=data.get("arbeitsort", {}).get("plz"),
                        published_date=data.get("eintrittsdatum"),
                        description=data.get("stellenbeschreibung", ""),
                    )
            except httpx.HTTPError:
                return None
        return None


if __name__ == "__main__":
    async def demo():
        client = JobsucheClient()
        print("Initialized Jobsuche Client with bundesAPI/jobsuche-api patterns.")
    asyncio.run(demo())
