"""Wrapper for the LinkedIn scraper integration."""
from services.linkedin_scraper.main import run_linkedin_scraper


def sync_linkedin_jobs() -> None:
    """Kick off the LinkedIn scraping job."""
    run_linkedin_scraper()
