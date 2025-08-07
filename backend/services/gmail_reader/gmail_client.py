import json
from urllib import response
import requests
from datetime import datetime
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SERVICE_NAME = "gmail_service"
SERVICE_SECRET = "gmail_secret"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIAL_ENDPOINT = 'http://localhost:8000/google-creds/all'
SERVICE_TOKEN_ENDPOINT = 'http://localhost:8001/auth/token'

def get_service_auth_token():
    """
    Retrieves the service auth token from environment variables or a config file.
    """
    response = requests.post(SERVICE_TOKEN_ENDPOINT, json={
        "service_name": SERVICE_NAME,
        "service_secret": SERVICE_SECRET
    })
    if response.status_code == 200:
        return response.json().get("access_token")
    raise Exception("Failed to retrieve service auth token")

def load_credentials() -> dict:
    service_token = get_service_auth_token()
    headers = {
        "Authorization": f"Bearer {service_token}"
    }
    response = requests.get(CREDENTIAL_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {}

def get_gmail_services():
    """
    Returns a dict of {email: gmail_service} for every credentials entry in credentials.json
    """
    all_credentials = load_credentials()

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

