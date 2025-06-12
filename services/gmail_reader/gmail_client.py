import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service():
    credentials_path = os.path.join(BASE_DIR, "credentials.json")

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            "credentials.json not found. Please authenticate first.")

    with open(credentials_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    # client_id = data.get("client_id")
    # client_secret = data.get("client_secret")
    # token_uri = data.get("token_uri", "https://oauth2.googleapis.com/token")

    if not access_token:
        raise ValueError("access_token not found in credentials.json")

    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        # client_id=client_id,
        # client_secret=client_secret,
        # token_uri=token_uri,
        scopes=SCOPES
    )

    service = build("gmail", "v1", credentials=creds)
    return service


def get_gmail_services():
    """
    Returns a dict of {email: gmail_service} for every credentials entry in credentials.json
    """
    credentials_path = os.path.join(BASE_DIR, "credentials.json")
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            "credentials.json not found. Please authenticate first.")

    with open(credentials_path, "r", encoding="utf-8") as f:
        all_credentials = json.load(f)

    services = {}
    for email, creds_data in all_credentials.items():
        access_token = creds_data.get("access_token")
        refresh_token = creds_data.get("refresh_token")
        if not access_token:
            continue
        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            scopes=SCOPES
        )
        service = build("gmail", "v1", credentials=creds)
        services[email] = service
    return services
