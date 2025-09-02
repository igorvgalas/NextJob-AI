import json
import os
from gmail_client import get_gmail_services
from publisher import publish_job
from utils import extract_email_body, get_header_value

class GmailJobFetcher:
    KEYWORDS = ['job', 'vacancy', 'hiring', 'position', 'remote', 'pracuj', 'oferta', 'oferty']
    PROCESSED_FILE = "output/processed_ids.json"

    def __init__(self):
        self.processed_ids = self._load_processed_ids()
        self.new_ids = set()
        self.services = get_gmail_services()  # {email: service}

    def _load_processed_ids(self):
        if os.path.exists(self.PROCESSED_FILE):
            with open(self.PROCESSED_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        return set()

    def _save_processed_ids(self):
        os.makedirs(os.path.dirname(self.PROCESSED_FILE), exist_ok=True)
        with open(self.PROCESSED_FILE, "w", encoding="utf-8") as f:
            json.dump(list(self.processed_ids), f, indent=2)

    def _contains_keywords(self, text):
        return any(kw.lower() in text.lower() for kw in self.KEYWORDS)

    def process_emails(self):
        for email, service in self.services.items():
            print(f"Checking emails for {email}")
            results = service.users().messages().list(userId='me', maxResults=100).execute()

            if 'messages' not in results:
                print(f"No messages found for {email}.")
                continue

            for msg in results.get('messages', []):
                msg_id = msg['id']
                if msg_id in self.processed_ids:
                    print(f"Skipping already processed message {msg_id} for {email}")
                    continue

                msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                headers = msg_data.get('payload', {}).get('headers', [])
                full_text = extract_email_body(msg_data)
                subject = get_header_value(headers, 'Subject') or ''

                if not full_text:
                    continue

                if self._contains_keywords(full_text) or self._contains_keywords(subject):
                    publish_job({
                        'email': email,
                        'subject': get_header_value(headers, 'From') or '',
                        'full_text': full_text,
                        'id': msg_id,
                    })
                    self.new_ids.add(msg_id)
                    print(f"Published new job from message {msg_id} for {email}")
                else:
                    print(f"No keywords found in message {msg_id} for {email}, skipped")

        self._finalize()

    def _finalize(self):
        self.processed_ids.update(self.new_ids)
        self._save_processed_ids()
        print(f"Saved {len(self.new_ids)} new processed message IDs.")


if __name__ == "__main__":
    fetcher = GmailJobFetcher()
    fetcher.process_emails()
