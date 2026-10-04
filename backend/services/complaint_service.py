from backend.agents.complaint_agent import complaint_agent


def generate_case_complaint(case_data: dict, police_station: str = "[Local Police Station]") -> dict:
    draft = complaint_agent(case_data, police_station)
    return {
        "document_type": "Police Complaint Draft",
        "draft_text": draft
    }