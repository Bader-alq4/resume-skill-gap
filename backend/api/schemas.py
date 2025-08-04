from pydantic import BaseModel
from typing import List, Dict, Optional

class SimilarityDetail(BaseModel):
    matched_skill: str
    score: float

class AnalyzeResponse(BaseModel):
    match_score: float
    user_skills: List[str]
    job_skills: List[str]  
    missing_skills: List[str]
    recommendations: Dict[str, List[str]]
    similarity_details: Optional[Dict[str, SimilarityDetail]] = None