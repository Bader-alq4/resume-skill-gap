import json
from pathlib import Path # safer and cleaner way to handle file paths than regular strings
import numpy as np
from .embedder import get_embeddings

ROLES_PATH = Path(__file__).parent.parent / "roles.json"

# Load job roles and their required skills from roles.json
# Returns a dictionary like: { "Data Scientist": ["Python", "SQL", ...], ... }
def load_role_skills(path: Path = ROLES_PATH) -> dict[str, list[str]]:
    with open(path, "r") as f:
        return json.load(f)
    

def compute_missing(user_skills: list[str], role_skills: list[str], threshold: float = 0.8) -> list[str]:
    """
    Return list of role skills that are not semantically similar to any user skill.
    Uses cosine similarity to find best matches. Anything below threshold is 'missing'.
    """
    if not role_skills or not user_skills:
        return sorted(role_skills)

    # Get embeddings
    all_skills = list(set(user_skills + role_skills))
    embeddings = get_embeddings(all_skills)
    skill_to_index = {s: i for i, s in enumerate(all_skills)}

    missing = []

    for role_skill in role_skills:
        best_score = 0.0
        r_idx = skill_to_index[role_skill]
        r_vec = embeddings[r_idx]
        r_norm = np.linalg.norm(r_vec)

        for user_skill in user_skills:
            # Case-insensitive exact match → full credit
            if user_skill.strip().lower() == role_skill.strip().lower():
                best_score = 1.0
                break

            u_idx = skill_to_index[user_skill]
            u_vec = embeddings[u_idx]
            u_norm = np.linalg.norm(u_vec)

            sim = float(np.dot(r_vec, u_vec) / (r_norm * u_norm + 1e-8))
            best_score = max(best_score, sim)

        if best_score < threshold:
            missing.append(role_skill)

    return sorted(missing)

def compute_per_skill_score(user_skills: list[str], role_skills: list[str]) -> float:
    """
    Compute a semantic match score between user_skills and role_skills by averaging
    the best cosine similarity for each required skill.
    Exact string matches (case-insensitive) get full credit.
    Returns a percentage (0.0 to 100.0).
    """
    if not role_skills or not user_skills:
        return 0.0

    # Embed all unique skills
    all_skills = list({s for s in user_skills + role_skills})
    embeds = get_embeddings(all_skills)
    idx = {skill: i for i, skill in enumerate(all_skills)}

    # Precompute norms
    norms = np.linalg.norm(embeds, axis=1)

    # Compute per-role-skill similarity
    sims = []
    for r in role_skills:
        r_idx = idx[r]
        r_vec = embeds[r_idx]
        r_norm = norms[r_idx]

        best = 0.0
        for u in user_skills:
            # Case-insensitive exact match
            if u.strip().lower() == r.strip().lower():
                best = 1.0
                break
            u_idx = idx[u]
            u_vec = embeds[u_idx]
            u_norm = norms[u_idx]
            sim = float(np.dot(r_vec, u_vec) / (r_norm * u_norm + 1e-8))
            best = max(best, sim)
        sims.append(best)

    score = float(np.mean(sims)) * 100.0
    return round(score, 2)



def compute_similarity_details(
    user_skills: list[str],
    job_skills: list[str]
) -> dict[str, dict[str, float | str]]:
    """
    For each job_skill, compute:
      - which user_skill gave the highest cosine sim
      - that sim (%) rounded to 2 decimals
    """
    # 1. Embed every unique skill once
    all_skills = list({*user_skills, *job_skills})
    embeds = get_embeddings(all_skills)
    idx = {skill: i for i, skill in enumerate(all_skills)}
    norms = np.linalg.norm(embeds, axis=1)

    details: dict[str, dict[str, float | str]] = {}
    for js in job_skills:
        r_vec = embeds[idx[js]]
        r_norm = norms[idx[js]]
        best_sim = 0.0
        best_match = None
        for us in user_skills:
            u_vec = embeds[idx[us]]
            u_norm = norms[idx[us]]
            sim = float(np.dot(r_vec, u_vec) / (r_norm * u_norm + 1e-8))
            if sim > best_sim:
                best_sim = sim
                best_match = us
        details[js] = {
            "matched_skill": best_match or "",
            "score": round(best_sim * 100, 2)   # percent
        }
    return details


def compute_match_score(user_skills: list[str], role_skills: list[str]) -> float:
    """
    Alias to compute_per_skill_score for backward compatibility.
    """
    return compute_per_skill_score(user_skills, role_skills)