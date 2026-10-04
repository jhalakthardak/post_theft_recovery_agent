from sqlalchemy.orm import Session
from .models import CaseModel


def create_case_record(db: Session, case_id: str, report_data: dict, risk_data: dict, checklist_data: list):
    case_obj = CaseModel(
        case_id=case_id,
        user_name=report_data.get("user_name"),
        incident_location=report_data.get("incident_location"),
        incident_date=report_data.get("incident_date"),
        theft_type=report_data.get("theft_type"),
        report_details=report_data,
        risk_assessment=risk_data,
        checklist=checklist_data
    )
    db.add(case_obj)
    db.commit()
    db.refresh(case_obj)
    return case_obj


def get_case_by_id(db: Session, case_id: str):
    return db.query(CaseModel).filter(CaseModel.case_id == case_id).first()


def update_case_checklist(db: Session, case_id: str, updated_checklist: list):
    case_obj = get_case_by_id(db, case_id)
    if case_obj:
        case_obj.checklist = updated_checklist
        db.commit()
        db.refresh(case_obj)
    return case_obj