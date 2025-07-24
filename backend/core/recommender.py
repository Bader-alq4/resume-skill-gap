import os
import json 

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError, RateLimitError # OpenAI client and error handling

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# tells the LLM exactly how to behave and format output
SYSTEM_PROMPT = """
You are a JSON-only career advisor. When given a list of missing skills,
you must reply *exactly* with a single JSON object and *nothing else*.
Do not provide any extra text or markdown.

Example format:
User: The user is missing these skills: Pandas, SQL.
Assistant:
{
  "courses": ["Intro to Pandas", "SQL for Data Analysis", "Data Engineering Fundamentals"],
  "projects": ["Analyze sales data with Pandas", "Build a SQL dashboard", "ETL pipeline project"],
  "certifications": ["Pandas Certification", "SQL Certification", "Data Engineering Certificate"]
}

Now, respond in that exact JSON-only format.
"""

# This template will be filled in with the user’s actual missing skills
USER_TEMPLATE = "The user is missing these skills: {skills}."


def get_recommendations(missing: list[str]) -> dict:
    # If there are no missing skills, return empty recommendations
    if not missing:
        return {
            "courses": [],
            "projects": [],
            "certifications": []
        }

    # Format system/user messages for OpenAI Chat API
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
        {"role": "user", "content": USER_TEMPLATE.format(skills=", ".join(missing))}
    ]

    try:
        # Call OpenAI ChatCompletion with deterministic settings (no randomness)
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.0,     # zero randomness
            top_p=1.0,           # full probability mass
            max_tokens=250       # limit output size
        )

        # Extract and trim the output string
        content = resp.choices[0].message.content.strip()

        # Ensure output starts/ends like a valid JSON object
        if not (content.startswith("{") and content.endswith("}")):
            raise ValueError(f"Unexpected format: {content!r}")

        # Parse and return JSON object
        return json.loads(content)

    except (RateLimitError, OpenAIError) as e:
        # Handles rate limit or other API issues
        return {
            "courses": [f"[LLM error: {e}]"],
            "projects": [],
            "certifications": []
        }
    
    except (ValueError, json.JSONDecodeError):
        # Handles JSON parsing issues if model responds badly
        return {
            "courses": ["[Failed to parse LLM output — ensure it’s valid JSON]"],
            "projects": [],
            "certifications": []
        }