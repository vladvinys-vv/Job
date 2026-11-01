import pytest
import httpx
from unittest.mock import AsyncMock, patch
from src.jobsuche_client import JobsucheClient, JobPosting
from src.job_tracker import JobTrackerDB


def test_job_posting_dataclass():
    posting = JobPosting(
        job_id="10001-TEST",
        title="Softwareentwickler Python",
        employer="Tech Solutions GmbH",
        city="Berlin",
        postal_code="10115",
        employment_type="Vollzeit",
    )
    assert posting.job_id == "10001-TEST"
    assert posting.employer == "Tech Solutions GmbH"
    assert posting.employment_type == "Vollzeit"


def test_job_tracker_db(tmp_path):
    test_db_path = str(tmp_path / "test_jobs.db")
    tracker = JobTrackerDB(db_path=test_db_path)

    # 1. Add job
    tracker.add_job(
        job_id="12345",
        title="Fullstack Developer",
        company="Startup AG",
        city="Hamburg",
        notes="Applied via portal",
    )

    apps = tracker.list_applications()
    assert len(apps) == 1
    assert apps[0].job_id == "12345"
    assert apps[0].status == "FOUND"

    # 2. Get single job
    job = tracker.get_job("12345")
    assert job is not None
    assert job.title == "Fullstack Developer"
    assert tracker.get_job("non-existent") is None

    # 3. Update status
    tracker.update_status(job_id="12345", status="APPLIED", notes="Interview scheduled")
    applied_apps = tracker.list_applications(status="APPLIED")
    assert len(applied_apps) == 1
    assert applied_apps[0].status == "APPLIED"
    assert "Interview" in applied_apps[0].notes

    # 4. Delete job
    deleted = tracker.delete_job("12345")
    assert deleted is True
    assert tracker.get_job("12345") is None
    assert tracker.delete_job("12345") is False
    assert len(tracker.list_applications()) == 0


@pytest.mark.asyncio
async def test_jobsuche_client_mocked():
    client = JobsucheClient(timeout=0.1)
    assert client.timeout == 0.1
    assert "X-API-Key" in client.headers

    mock_response_data = {
        "stellenangebote": [
            {
                "refnr": "BA-1002",
                "titel": "Python Backend Engineer",
                "arbeitgeber": "Innovate Tech GmbH",
                "arbeitsort": {"ort": "Berlin", "plz": "10115"},
                "aktuelleVeroeffentlichungsdatum": "2026-10-28",
                "arbeitszeit": "Vollzeit",
            }
        ]
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = httpx.Response(
            200,
            json=mock_response_data,
            request=httpx.Request("GET", "https://rest.arbeitsagentur.de/infosysbub/jobboerse/pc/v4/jobs"),
        )

        results = await client.search_jobs("Python", location="Berlin")
        assert len(results) == 1
        assert results[0].job_id == "BA-1002"
        assert results[0].employer == "Innovate Tech GmbH"
        assert results[0].city == "Berlin"
