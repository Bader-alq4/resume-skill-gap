from backend.core.parser import extract_user_skills_manual, load_known_skills

'''
Extract skills from manual skills input.

'''
def test_manual_input_parser():
    known = load_known_skills()
    typed = "pyhton, docker-compose, javscript,  seql,  "

    skills = extract_user_skills_manual(typed, known)

    # Expected normalized skills (adjust to match your parser behavior)
    expected_subset = {"Python", "Docker", "JavaScript", "SQL"}

    # Ensure at least these core skills are detected
    assert expected_subset.issubset(set(skills)), f"Parsed skills: {skills}"

    # Check that parser returns non-empty normalized list
    assert len(skills) > 0
