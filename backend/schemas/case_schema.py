from pydantic import BaseModel, Field
from typing import Optional, List
from .theft_schema import TheftReportCreate
from .risk_schema import RiskAssessmentOutput
from .task_schema import TaskItem


class CaseResponse(BaseModel):
    case_id: str
    created_at: str
    status: str
    report_details: TheftReportCreate
    risk_assessment: Optional[RiskAssessmentOutput] = None
    checklist: List[TaskItem] = Field(default_factory=list)