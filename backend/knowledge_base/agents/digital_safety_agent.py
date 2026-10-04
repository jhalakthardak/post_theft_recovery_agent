def digital_safety_agent(mobile_data: dict) -> list:
    """
    Provides account security instructions for stolen mobile devices.
    """
    steps = []
    if mobile_data.get("has_email_access"):
        steps.append("Log out of all active email sessions remotely (Google Security / Apple ID).")
    if mobile_data.get("has_upi"):
        steps.append("Deregister UPI handles by calling bank / UPI helpline (1930).")
    steps.append("Revoke active session tokens for social media and messaging apps.")

    return steps