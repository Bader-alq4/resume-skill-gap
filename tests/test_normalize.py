import pytest

from backend.core.parser import normalize_skill, load_known_skills

'''
Normalize a raw skill string to a consistent canonical form

'''

def test_normalize_skill_variants():
    known = load_known_skills()
    
    samples = {
        "pyhton": "Python",
        "docker-compose": "Docker",
        "Javascript": "JavaScript",
        "Machine-Learn": "Machine Learning",
        "K8s": "K8s",  # fallback to original
    }
    
    for raw, expected in samples.items():
        normalized = normalize_skill(raw, known)
        # Normalize K8s as fallback if not in known
        if raw == "K8s" and normalized == raw:
            continue
        assert normalized == expected, f"{raw} normalized to {normalized}, expected {expected}"
