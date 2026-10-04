def risk_agent(structured_case: dict) -> dict:
    """
    Evaluates financial, digital, and identity risk levels.
    """
    cards = structured_case.get("cards_exposed", [])
    docs = structured_case.get("missing_documents", [])
    mobile = structured_case.get("mobile", {})

    reasons = []
    score = 0

    # Financial Risk Assessment
    if cards:
        score += 4
        reasons.append(f"Exposed payment cards ({', '.join(cards)})")
    if mobile.get("has_banking_apps") or mobile.get("has_upi"):
        score += 4
        reasons.append("Stolen device contains UPI / active banking app sessions")

    # Identity Risk Assessment
    if docs:
        score += len(docs) * 2
        reasons.append(f"Lost government identity documents ({', '.join(docs)})")

    # Digital Security Risk
    if mobile.get("sim_present"):
        score += 2
        reasons.append("Active SIM card in stolen device enables SMS OTP interception")

    # Risk Level Categorization
    fin_risk = "HIGH" if (cards or mobile.get("has_upi")) else "LOW"
    id_risk = "HIGH" if len(docs) >= 2 else ("MEDIUM" if docs else "LOW")
    dig_risk = "HIGH" if mobile.get("sim_present") else "LOW"

    return {
        "financial_risk": fin_risk,
        "identity_risk": id_risk,
        "digital_risk": dig_risk,
        "overall_score": score,
        "reasons": reasons
    }