import json
import httpx
import redis
import requests
import asyncio
from analyzer import analyze_job

r = redis.Redis(host="localhost", port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe("jobs")

print("Listening for job offers...")

BUFFER_SIZE = 5
job_buffer = []

API_URL = "http://0.0.0.0:8000/job_offers/bulk_create"
SERVICE_NAME = "digest_generator"
SERVICE_SECRET = "digest_generator_secret"
SERVICE_TOKEN_ENDPOINT = "http://localhost:8001/auth/token"

async def fetch(url: str, params: dict | None = None):
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
async def get_service_auth_token():
    """
    Retrieves the service auth token from environment variables or a config file.
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                SERVICE_TOKEN_ENDPOINT,
                data={"service_name": SERVICE_NAME, "service_secret": SERVICE_SECRET},
            )
            response.raise_for_status()
            token_data = response.json()
            return token_data.get("access_token", "")
    except httpx.RequestError as e:
        print(f"Error fetching service auth token: {e}")
        return ""

async def fetch_user_tech_stack(user_id: int) -> list[str]:
    url = f"http://localhost:8000/users/{user_id}/tech_stack"
    try:
        tech_stack_data = await fetch(url)
        return tech_stack_data.get("tech_stack", [])
    except httpx.HTTPError as e:
        print(f"Error fetching user tech stack: {e}")
        return []

async def send_bulk_to_api(jobs: list[dict]):
    token = await get_service_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(API_URL, json={"jobs": jobs}, headers=headers)
            response.raise_for_status()
            print(f"✅ Successfully sent {len(jobs)} job offers to API.")
    except httpx.HTTPError as e:
        print(f"Error sending job offers to API: {e}")

async def analyze_and_send(jobs: list[dict]) -> None:
    print(f"\n🔎 Analyzing {len(jobs)} job offers...")
    # Pass the list of job objects directly to analyze_job
    tech_stack = await fetch_user_tech_stack(user_id=1) # Replace with actual user ID
    if not tech_stack:
        print("No user tech stack found, skipping analysis.")
        return
    analysis_result = analyze_job({"jobs": jobs}, tech_stack)

    if not analysis_result:
        print("No valid analysis result returned")
        return

    print("Analysis result:")
    # print(json.dumps(analysis_result, indent=2))

    job_results = analysis_result.get("results", [])
    if job_results:
        await send_bulk_to_api(job_results)
    else:
        print("⚠️ No job results found in analysis output.")


print("Ready to receive messages...")

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
        print("Invalid JSON:", raw_data)
    # Analyze and POST every BUFFER_SIZE jobs
    if len(job_buffer) >= BUFFER_SIZE:
        asyncio.run(analyze_and_send(job_buffer))
        job_buffer.clear()

