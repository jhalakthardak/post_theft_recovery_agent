def complaint_agent(case_data: dict, police_station: str = "[Local Police Station]") -> str:
    """
    Generates a personalized police complaint draft.
    """
    user_name = case_data.get("user_name", "[Your Name]")
    location = case_data.get("incident_location", "[Incident Location]")
    date = case_data.get("incident_date", "[Incident Date]")
    description = case_data.get("description", "")

    draft = f"""To,
The Officer-in-Charge,
{police_station}

Subject: Report regarding theft of wallet / mobile phone and identity documents

Respected Sir/Madam,

I, {user_name}, am writing to formally report an incident of theft that occurred on {date} at or near {location}.

Incident Details:
{description if description else "My wallet/mobile device containing personal belongings and identity cards was stolen."}

I request you to register this complaint and issue an official acknowledgment / Loss Certificate to enable me to process document re-issuance and prevent unauthorized misuse of my assets.

Thank you.

Yours faithfully,
{user_name}
Date: {date}
"""
    return draft.strip()