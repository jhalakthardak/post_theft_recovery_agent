from pydantic import BaseModel
from typing import List, Dict


class DeviceSecurityGuidance(BaseModel):
    device_type: str
    lock_portal_url: str
    ceir_portal_url: str
    action_steps: List[str]
    authorized_redirects: Dict[str, str]