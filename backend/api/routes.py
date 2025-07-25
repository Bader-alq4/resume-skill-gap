from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional

from backend.core.parser import load_known_skills

from backend.core.parser import (
    extract_text_from_pdf,
    extract_skills,
    extract_user_skills_manual,
)
from backend.core.analyzer import (
    load_role_skills,
    compute_match_score,
    compute_missing,
)
from backend.core.recommender import get_recommendations
from .schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()

# Load role definitions once at startup
roles_map = load_role_skills()


@router.get("/roles", response_model=List[str])
def list_roles():
    """
    Return all available role names for the frontend dropdown.
    """
    return list(roles_map.keys())


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: Optional[UploadFile] = File(None),
    role: str = Form(...),
    manual_skills: Optional[str] = Form(None),
):
    """
    Analyze a resume PDF or manual skills list against a chosen role.
    Returns match score, extracted or manual user skills, missing skills, and LLM recommendations.
    """

    # Step 1: Get user skills from either resume or manual input
    if file:
        pdf_bytes = await file.read()
        text = extract_text_from_pdf(pdf_bytes)

        # Build flat list of known skills for normalization
        known_skills = load_known_skills()
        user_skills = extract_skills(text, known_skills)
    else:
        if not manual_skills:
            raise HTTPException(status_code=400, detail="Manual skills input is missing")

        # Build flat list of known skills for normalization
        known_skills = load_known_skills()
        user_skills = extract_user_skills_manual(manual_skills, known_skills)

    # Step 2: Validate role
    if role not in roles_map:
        raise HTTPException(status_code=400, detail="Unknown role")

    # Step 3: Analyze
    role_skills = roles_map[role]
    score = compute_match_score(user_skills, role_skills)
    missing = compute_missing(user_skills, role_skills)
    recs = get_recommendations(missing)

    # Step 4: Return response
    return AnalyzeResponse(
        match_score=score,
        user_skills=user_skills,
        missing_skills=missing,
        recommendations=recs,
    )
