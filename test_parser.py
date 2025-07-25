from backend.core.parser import parse_resume, load_known_skills

with open("BaderAlqasem_resume.pdf", "rb") as f:
    resume_bytes = f.read()

skills = parse_resume(resume_bytes, load_known_skills())
print("Extracted skills:", skills)



# # Manual input test
# from backend.core.parser import extract_user_skills_manual, load_known_skills

# known = load_known_skills()
# typed = "pyhton, docker-compose, javscript,  seql,  "

# skills = extract_user_skills_manual(typed, known)
# print("Manual input normalized:", skills)
