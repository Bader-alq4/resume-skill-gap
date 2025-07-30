# Manual input test
from backend.core.parser import extract_user_skills_manual, load_known_skills

known = load_known_skills()
typed = "pyhton, docker-compose, javscript,  seql,  "

skills = extract_user_skills_manual(typed, known)
print("Manual input normalized:", skills)