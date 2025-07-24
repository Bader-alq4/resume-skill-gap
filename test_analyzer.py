# test_analyzer.py

from backend.core.analyzer import (
    load_role_skills,
    compute_missing,
    compute_match_score
)

# Simulate user input
user_skills = ["Python", "SQL", "Scikit learn", "TensorFlow", "Maths"]

# Load roles and choose one
roles = load_role_skills()
target_role = "Data Scientist"
role_skills = roles.get(target_role, [])

# Run analyzer
missing = compute_missing(user_skills, role_skills)
match_score = compute_match_score(user_skills, role_skills)

# Output results
print(f"Target Role: {target_role}")
print(f"User Skills: {user_skills}")
print(f"Role Skills: {role_skills}")
print(f"Match Score: {match_score}%")
print(f"Missing Skills: {missing}")
