from pydantic import BaseModel
from typing import List, Dict

class AnalyzeResponse(BaseModel):
    match_score: float
    user_skills: List[str]
    missing_skills: List[str]
    recommendations: Dict[str, List[str]]