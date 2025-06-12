import json
import os
from gmail_client import get_gmail_services
from publisher import publish_job
from utils import extract_email_body, get_header_value

KEYWORDS = ['job', 'vacancy', 'hiring', 'position', 'remote']
PROCESSED_FILE = "output/processed_ids.json"


def load_processed_ids():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_processed_ids(ids):
    os.makedirs("output", exist_ok=True)
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f, indent=2)


def fetch_recent_emails():
    services = get_gmail_services()  # {email: gmail_service}
    for email, service in services.items():
        results = (
            service.users()
            .messages()
            .list(userId='me', maxResults=100)
            .execute()
        )

        if 'messages' not in results:
            print(f"📭 No messages found for {email}.")
            continue

        processed_ids = load_processed_ids()
        new_ids = set()

        for msg in results.get('messages', []):
            msg_id = msg['id']
            if msg_id in processed_ids:
                print(
                    f"⏩ Skipping already processed message {msg_id} for {email}")
                continue

            msg_data = (
                service.users()
                .messages()
                .get(userId='me', id=msg_id, format='full')
                .execute()
            )
            headers = msg_data.get('payload', {}).get('headers', [])
            full_text = extract_email_body(msg_data)

            if not full_text:
                continue

            if any(kw.lower() in full_text.lower() for kw in KEYWORDS):
                publish_job({
                    'email': email,
                    'subject': get_header_value(headers, 'From') or '',
                    'full_text': full_text,
                    'id': msg_id,
                })
                new_ids.add(msg_id)
                print(f"✅ Published new job from message {msg_id} for {email}")
            else:
                print(
                    f"❌ No keywords found in message {msg_id} for {email}, skipped")

        processed_ids.update(new_ids)
        save_processed_ids(processed_ids)


if __name__ == "__main__":
    fetch_recent_emails()
