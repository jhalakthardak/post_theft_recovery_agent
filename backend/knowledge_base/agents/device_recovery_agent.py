def device_recovery_agent(device_type: str = "Android") -> dict:
    """
    Provides authorized device security and locking routes.
    """
    if device_type.lower() == "iphone":
        lock_url = "https://www.icloud.com/find"
    else:
        lock_url = "https://www.google.com/android/find/"

    return {
        "device_type": device_type,
        "lock_portal_url": lock_url,
        "ceir_portal_url": "https://ceir.gov.in/",
        "instructions": [
            "Use official device locator to remote-lock handset.",
            "Block handset IMEI on CEIR portal to restrict network access nationwide."
        ]
    }