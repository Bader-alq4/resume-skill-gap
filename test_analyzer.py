from backend.core.analyzer import analyze_user_skills

user_skills = ["Python", "SQL", "Docker"]
result = analyze_user_skills(user_skills, "Data Scientist")

print(result)