import json
from backend.core.parser import parse_resume

with open("BaderAlqasem_resume.pdf", "rb") as f:
    pdf_bytes = f.read()

with open("backend/known_skills.json") as f:
    known_skills = json.load(f)

skills = parse_resume(pdf_bytes, known_skills)
print("Extracted skills:", skills)
