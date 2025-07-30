from pathlib import Path
from backend.core.parser import parse_resume, load_known_skills

'''
Extract skills from a resume PDF.

'''

def test_parse_resume_extracts_skills():
    # Use a small dummy PDF for CI instead of your real resume
    pdf_path = Path(__file__).parent / "fixtures" / "sample_resume.pdf"
    assert pdf_path.exists(), "Sample resume PDF is missing for the test."

    with open(pdf_path, "rb") as f:
        resume_bytes = f.read()

    skills = parse_resume(resume_bytes, load_known_skills())

    # Assert that we got at least one skill
    assert isinstance(skills, list), "parse_resume should return a list"
    assert all(isinstance(s, str) for s in skills), "All skills should be strings"
    assert len(skills) > 0, "Expected at least one skill from the sample resume"
