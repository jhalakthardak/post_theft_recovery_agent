from pydantic import BaseModel
from typing import List


class RiskAssessmentOutput(BaseModel):
    financial_risk: str  # LOW, MEDIUM, HIGH, CRITICAL
    identity_risk: str   # LOW, MEDIUM, HIGH, CRITICAL
    digital_risk: str    # LOW, MEDIUM, HIGH, CRITICAL
    overall_score: int
    reasons: List[str]