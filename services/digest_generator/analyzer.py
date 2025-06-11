from dotenv import load_dotenv
from g4f.client import Client
import json

load_dotenv()

TARGET_TECH = [
    "Python",
    "Django",
    "React",
    "PostgreSQL",
    "Docker",
    "GitHub Actions",
    "CI/CD",
    "Azure/AD integrations",
    "DevOps practices",
    "REST APIs with DRF",
    "Experience with both Linux & Windows environments"
]


def build_prompt(job_text):
    tech_stack = ", ".join(TARGET_TECH)
    return f"""
You are a job search assistant.

This is a list of new job opportunities:
{job_text}

The user has the following tech stack: {tech_stack}

For each job, please analyze:

- Does it match the stack?
- Can a person with this stack reasonably apply?
- Is the job likely still available?
- Is the job description clear and detailed?

Respond with a single **valid JSON object** that includes a key `"results"` which contains a **list of structured job offers**, one per job, in the following format:

{{
  "results": [
    {{
      "match_score": "1-10 (1 = no match, 10 = perfect match) it should be a number",
      "reason": "detailed explanation of the match score",
      "technologies_matched": ["list", "of", "technologies", "from", "description"],
      "title": "Extracted job title",
      "company": "Extracted company name (if available)",
      "location": "Extracted job location",
      "apply_link": "Direct link to apply or full job page URL"
    }},
    ...
  ]
}}

Important:
- Always return **valid JSON** (no markdown, no comments).
- Do **not include any additional explanation** or text outside the JSON.
"""


def analyze_job(job_text):
    prompt = build_prompt(job_text)
    print(f"🔍 Analyzing job offer with g4f for:\n{prompt}\n")

    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",  # You can also try "gpt-4o" or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )
        content = response.choices[0].message.content.strip()
    except Exception as e:  # pylint: disable=broad-except
        print("❌ Error from g4f client:", e)
        return None
    if content.startswith("```json"):
        content = content.removeprefix("```json").removesuffix("```").strip()
    elif content.startswith("```"):
        content = content.removeprefix("```").removesuffix("```").strip()
    # Parse JSON response
    try:
        return json.loads(content)
    except Exception:  # pylint: disable=broad-except
        print("❌ Failed to parse GPT response:", content)
        return None
