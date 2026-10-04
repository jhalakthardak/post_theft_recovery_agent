import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from .database import Base


class CaseModel(Base):
    __tablename__ = "cases"

    case_id = Column(String, primary_key=True, index=True)
    created_at = Column(String, default=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = Column(String, default="Active")
    user_name = Column(String)
    incident_location = Column(String)
    incident_date = Column(String)
    theft_type = Column(String)  # wallet, mobile, both
    report_details = Column(JSON)
    risk_assessment = Column(JSON, nullable=True)
    checklist = Column(JSON, default=list)