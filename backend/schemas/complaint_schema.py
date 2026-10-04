from pydantic import BaseModel


class ComplaintDraftRequest(BaseModel):
    case_id: str
    police_station_name: str = "[Local Police Station]"
    additional_notes: str = ""


class ComplaintDraftResponse(BaseModel):
    case_id: str
    document_type: str
    draft_text: str