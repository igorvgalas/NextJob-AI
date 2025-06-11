import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0)

def publish_job(job_data: dict):
    message = json.dumps(job_data)
    r.publish('jobs', message)
