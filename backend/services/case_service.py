import uuid
from backend.agents.intake_agent import intake_agent
from backend.agents.risk_agent import risk_agent
from backend.agents.planning_agent import planning_agent


def process_new_case(report_data: dict) -> dict:
    case_id = f"CASE-{uuid.uuid4().hex[:6].upper()}"
    structured_case = intake_agent(report_data)
    risk = risk_agent(structured_case)
    checklist = planning_agent(structured_case, risk)

    return {
        "case_id": case_id,
        "status": "Active",
        "structured_case": structured_case,
        "risk_assessment": risk,
        "checklist": checklist
    }