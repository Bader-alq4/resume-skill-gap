from backend.core.parser import parse_resume, load_known_skills

with open("BaderAlqasem_resume.pdf", "rb") as f:
    resume_bytes = f.read()

skills = parse_resume(resume_bytes, load_known_skills())
print("Extracted skills:", skills)