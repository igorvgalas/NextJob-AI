import json

import redis
import requests
from analyzer import analyze_job

r = redis.Redis(host="localhost", port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe("jobs")

print("🔁 Listening for job offers...")

BUFFER_SIZE = 5
job_buffer = []

API_URL = "http://0.0.0.0:8000/job_offers/bulk_create"
SERVICE_NAME = "digest_generator"
SERVICE_SECRET = "digest_generator_secret"
SERVICE_TOKEN_ENDPOINT = "http://localhost:8001/auth/token"

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

def fetch_user_tech_stack(user_id: int) -> list[str]:
    try:
        response = requests.get(
            f"http://0.0.0.0:8000/service/user_skills/user/{user_id}",
            headers={"Authorization": f"Bearer {get_service_auth_token()}"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ Fetched user skills for user {user_id}: {data}")
        if isinstance(data, dict) and data:
            skills = data.get("skills", [])
            return [skill["name"] for skill in skills]
        else:
            print("⚠️ No user skills found")
            return []

    except requests.RequestException as e:
        print(f"❌ Failed to fetch user skills: {e}")
        return []

def send_bulk_to_api(jobs: list[dict]):
    try:
        response = requests.post(
            API_URL, json={"job_offers": jobs}, headers={"Authorization": f"Bearer {get_service_auth_token()}"}, timeout=10)
        if response.status_code == 201:
            print(f"✅ Sent {len(jobs)} jobs to API.")
        else:
            print(f"❌ API error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"❌ Failed to reach API: {e}")


def analyze_and_send(jobs: dict) -> None:
    print(f"\n🔎 Analyzing {len(jobs)} job offers...")
    # Pass the list of job objects directly to analyze_job
    tech_stack = fetch_user_tech_stack(user_id=1) # Replace with actual user ID
    if not tech_stack:
        print("⚠️ No user tech stack found, skipping analysis.")
        return
    analysis_result = analyze_job(jobs, tech_stack)

    if not analysis_result:
        print("❌ No valid analysis result returned")
        return

    print("✅ Analysis result:")
    # print(json.dumps(analysis_result, indent=2))

    job_results = analysis_result.get("results", [])
    if job_results:
        send_bulk_to_api(job_results)
    else:
        print("⚠️ No job results found in analysis output.")


print("🟢 Ready to receive messages...")

for message in pubsub.listen():
    if message["type"] != "message":
        continue

    raw_data = message["data"]
    if isinstance(raw_data, bytes):
        raw_data = raw_data.decode("utf-8")

    try:
        job_data = json.loads(raw_data)
        if "full_text" in job_data:
            job_buffer.append(job_data)
            print(f"📥 Job offer received ({len(job_buffer)}/{BUFFER_SIZE})")
        else:
            print("⚠️ Job offer missing 'full_text' field")

    except json.JSONDecodeError:
        print("❌ Invalid JSON:", raw_data)

    # Analyze and POST every BUFFER_SIZE jobs
    if len(job_buffer) >= BUFFER_SIZE:
        analyze_and_send(job_buffer)
        job_buffer.clear()
