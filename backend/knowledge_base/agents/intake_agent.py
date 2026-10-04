def intake_agent(raw_data: dict) -> dict:
    """
    Consolidates raw report inputs into a normalized structured case.
    """
    theft_type = raw_data.get("theft_type", "wallet")
    wallet = raw_data.get("wallet_details") or {}
    mobile = raw_data.get("mobile_details") or {}

    missing_documents = []
    if wallet.get("has_aadhaar"):
        missing_documents.append("Aadhaar")
    if wallet.get("has_pan"):
        missing_documents.append("PAN")
    if wallet.get("has_driving_licence"):
        missing_documents.append("Driving Licence")
    if wallet.get("has_voter_id"):
        missing_documents.append("Voter ID")

    cards = []
    if wallet.get("has_debit_card"):
        cards.append("Debit Card")
    if wallet.get("has_credit_card"):
        cards.append("Credit Card")

    return {
        "user_name": raw_data.get("user_name", "User"),
        "incident_location": raw_data.get("incident_location", "Unknown"),
        "incident_date": raw_data.get("incident_date", "Today"),
        "theft_type": theft_type,
        "missing_documents": missing_documents,
        "cards_exposed": cards,
        "mobile": mobile,
        "description": raw_data.get("description", "")
    }