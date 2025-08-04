from dotenv import load_dotenv
from g4f.client import Client
import json

load_dotenv()

def build_prompt(jobs: dict, tech_stack: list) -> str:
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

def analyze_job(jobs: dict, tech_stack: list) -> dict:
    prompt = build_prompt(jobs, tech_stack)
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
