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

API_URL = "http://0.0.0.0:8000/api/jobs/bulk_create/"
HEADERS = {
    "Content-Type": "application/json",
    # "Authorization": "Token <your-token>"  # optional
}


def send_bulk_to_api(jobs: list[dict]):
    try:
        response = requests.post(
            API_URL, json=jobs, headers=HEADERS, timeout=10)
        if response.status_code == 201:
            print(f"✅ Sent {len(jobs)} jobs to API.")
        else:
            print(f"❌ API error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"❌ Failed to reach API: {e}")


def analyze_and_send(jobs):
    print(f"\n🔎 Analyzing {len(jobs)} job offers...")
    # Pass the list of job objects directly to analyze_job
    analysis_result = analyze_job(jobs)

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
