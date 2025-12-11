"""Helpers to run the Gmail reader ingestion loop from inside the backend image."""
from services.gmail_reader.main import GmailJobFetcher


def run_gmail_ingestion() -> None:
    """Trigger Gmail ingestion using the existing service implementation."""
    fetcher = GmailJobFetcher()
    fetcher.process_emails()
