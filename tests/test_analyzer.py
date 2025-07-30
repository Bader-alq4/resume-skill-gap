import pytest

from backend.core.analyzer import (
    load_role_skills,
    compute_missing,
    compute_match_score
)

'''
Resposnible for skill matching and scoring

'''

def test_analyzer_data_scientist():
    user_skills = ["Python", "SQL", "Scikit learn", "TensorFlow", "Maths"]
    roles = load_role_skills()
    target_role = "Data Scientist"
    role_skills = roles.get(target_role, [])

    missing = compute_missing(user_skills, role_skills)
    match_score = compute_match_score(user_skills, role_skills)

    # ✅ CI assertions
    assert isinstance(match_score, (int, float)) and 0 <= match_score <= 100
    assert "Pandas", "Statistics" in missing
    assert match_score > 50