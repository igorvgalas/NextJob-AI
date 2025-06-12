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


# def build_prompt(job_text):
#     tech_stack = ", ".join(TARGET_TECH)
#     return f"""

# You are a job search assistant.

# This is a list of new job opportunities:
# {job_text}

# List contains an objects with the following fields:
# - `email`: Email address to whom the job is addressed
# - `full_text`: Full job description text
# - `subject`: Subject of the email (optional, can be empty)
# - `id`: Unique identifier of the job offer (optional, can be empty)

# The user has the following tech stack: {tech_stack}

# For each job, please analyze by criteria:

# - Does it match the stack?
# - Can a person with this stack reasonably apply?
# - Is the job likely still available?
# - Is the job description clear and detailed?
# - and other relevant factors.

# Respond with a single **valid JSON object** that includes a key `"results"` which contains a **list of structured job offers**, one per job, in the following format:

# {{
#   "results": [
#     {{
#       "email": "put here the exact email address from the job offer email field",
#       "match_score": "1-10 (1 = no match, 10 = perfect match) it should be a number",
#       "reason": "detailed analysis by criteria, explaining the match score",
#       "technologies_matched": ["list", "of", "technologies", "from", "description"],
#       "title": "Extracted job title",
#       "company": "Extracted company name (if available)",
#       "location": "Extracted job location",
#       "apply_link": "Direct link to apply or full job page URL"
#     }},
#     ...
#   ]
# }}

# Important:
# - Always return in results a list of objects that provide job offer information.
# - Always return **valid JSON** (no markdown, no comments).
# - Do **not include any additional explanation** or text outside the JSON.
# """
def build_prompt(jobs: dict) -> str:
    tech_stack = ", ".join(TARGET_TECH)
    return f"""
You are a job-search assistant.

INPUT
-----
jobs : {jobs}           ← array of job objects:
  • email      – target address
  • full_text  – full job description
  • subject    – email subject (may be empty)
  • id         – unique identifier (may be empty)

User tech stack: {tech_stack}

FILTER
------
Process **only** jobs that contain a meaningful description.  
Skip (do not output) any job if *either* of these is true:
  • full_text is empty OR fewer than 30 characters after trimming, **or**
  • full_text lacks any of: recognised job title, skills/stack keywords, or company name.  
If no jobs pass the filter, return `"results": []`.

TASK
----
For every job that passes the filter:
1. Assess match to the user’s tech stack.
2. Judge whether someone with this stack could reasonably apply.
3. Estimate if the job is still open.
4. Rate clarity/detail of the description.
5. Note any other relevant factors affecting fit.

OUTPUT
------
Return exactly one **valid JSON** object (no markdown, no comments) using this schema.
Leave unknown fields as empty strings.  Do not invent data.

{{
  "results": [
    {{
      "email": "<email from input>",
      "match_score": <integer 1-10>,
      "reason": "<brief justification of the score, touching on all criteria>",
      "technologies_matched": ["<tech 1>", "<tech 2>", ...],
      "title": "<extracted job title>",
      "company": "<extracted company name>",
      "location": "<extracted location>",
      "apply_link": "<direct application URL or full job post URL>"
    }},
    ...
  ]
}}

CONSTRAINTS
-----------
• Output must be valid, parseable JSON (UTF-8, no trailing commas).  
• No extra prose, markdown, or comments.  
• Ensure "match_score" is an integer 1–10.
"""

def analyze_job(jobs: dict) -> dict:
    prompt = build_prompt(jobs)
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
        return {}
    if content.startswith("```json"):
        content = content.removeprefix("```json").removesuffix("```").strip()
    elif content.startswith("```"):
        content = content.removeprefix("```").removesuffix("```").strip()
    # Parse JSON response
    try:
        return json.loads(content)
    except Exception:  # pylint: disable=broad-except
        print("❌ Failed to parse GPT response:", content)
        return {}
