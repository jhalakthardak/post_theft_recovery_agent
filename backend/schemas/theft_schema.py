from pydantic import BaseModel
from typing import List, Optional


class WalletTheftInput(BaseModel):
    has_aadhaar: bool = False
    has_pan: bool = False
    has_driving_licence: bool = False
    has_voter_id: bool = False
    has_debit_card: bool = False
    has_credit_card: bool = False
    has_cash: bool = False
    other_documents: List[str] = []


class MobileTheftInput(BaseModel):
    device_type: str = "Android"  # Android or iPhone
    sim_present: bool = True
    has_banking_apps: bool = False
    has_upi: bool = False
    has_email_access: bool = False
    tracking_enabled: bool = False


class TheftReportCreate(BaseModel):
    user_name: str
    incident_location: str
    incident_date: str
    description: Optional[str] = ""
    theft_type: str  # "wallet", "mobile", or "both"
    wallet_details: Optional[WalletTheftInput] = None
    mobile_details: Optional[MobileTheftInput] = None