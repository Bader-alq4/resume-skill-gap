import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def recommend_learning_path(missing_skills: list[str]) -> dict:
    """
    Ask OpenAI to suggest a course, project, and certification for each missing skill.
    Returns a dictionary with structured recommendations.
    """
    if not missing_skills:
        return {}

    skill_list = ", ".join(missing_skills)

    prompt = f"""
You are a career coach helping someone improve their technical skills.
For each of the following skills: {skill_list}, provide:

1. One recommended online course (just the name)
2. One project idea to practice it
3. One well-known certification (if available)

Return the result in this exact JSON format:
{{
  "Skill": {{
    "Course": "...",
    "Project": "...",
    "Certification": "..."
  }},
  ...
}}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    try:
        import json
        return json.loads(content)
    except Exception:
        return {"error": "Could not parse OpenAI response", "raw": content}
