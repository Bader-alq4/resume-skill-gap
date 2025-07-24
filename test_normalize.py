'''
pyhton → Python
docker-compose → Docker
Javascript → JavaScript
Machine-Learn → Machine Learning
K8s → K8s  # not found, fallback to original

'''

from backend.core.parser import normalize_skill, load_known_skills

known = load_known_skills()

for raw in ["pyhton", "docker-compose", "Javascript", "Machine-Learn", "K8s"]:
    print(f"{raw} → {normalize_skill(raw, known)}")
