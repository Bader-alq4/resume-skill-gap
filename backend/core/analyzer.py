import json
from pathlib import Path # safer and cleaner way to handle file paths than regular strings

ROLES_PATH = Path(__file__).parent.parent / "roles.json"

# Load job roles and their required skills from roles.json
# Returns a dictionary like: { "Data Scientist": ["Python", "SQL", ...], ... }
def load_role_skills(path: Path = ROLES_PATH) -> dict[str, list[str]]:
    with open(path, "r") as f:
        return json.load(f)


# Compare user's skills to the target role's required skills.
# Returns match %, matched skills, and missing skills.
def analyze_user_skills(user_skills: list[str], target_role: str) -> dict:

    all_roles = load_role_skills()
    required_skills = all_roles.get(target_role, [])

    matched = [skill for skill in required_skills if skill in user_skills]
    missing = [skill for skill in required_skills if skill not in user_skills]

    match_score = round(100 * len(matched) / len(required_skills)) if required_skills else 0

    return {
        "role": target_role,
        "match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing
    }
