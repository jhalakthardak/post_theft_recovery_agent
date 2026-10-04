def planning_agent(structured_case: dict, risk: dict) -> list:
    """
    Generates a dynamic recovery checklist based on lost items.
    """
    tasks = []
    task_id = 1

    # 1. Immediate Banking & Financial Actions
    if structured_case.get("cards_exposed") or structured_case.get("mobile", {}).get("has_upi"):
        tasks.append({
            "id": task_id,
            "title": "Block all exposed bank cards & freeze UPI handle",
            "priority": "URGENT",
            "category": "Banking",
            "completed": False,
            "instructions": "Call bank customer care immediately or use official banking portal to block cards."
        })
        task_id += 1

    # 2. Telecom / SIM Security
    if structured_case.get("mobile", {}).get("sim_present"):
        tasks.append({
            "id": task_id,
            "title": "Block stolen SIM card with telecom provider",
            "priority": "URGENT",
            "category": "SIM",
            "completed": False,
            "instructions": "Contact your telecom carrier to deactivate SIM and prevent OTP theft."
        })
        task_id += 1

    # 3. Device Recovery & Security
    if structured_case.get("theft_type") in ["mobile", "both"]:
        tasks.append({
            "id": task_id,
            "title": "Lock device and report IMEI on CEIR portal",
            "priority": "HIGH",
            "category": "Device",
            "completed": False,
            "instructions": "Use Google Find My / Apple Find My to lock device, then register IMEI on ceir.gov.in."
        })
        task_id += 1

    # 4. Legal / Police Report
    tasks.append({
        "id": task_id,
        "title": "File police complaint / Lost Article Report",
        "priority": "HIGH",
        "category": "Legal",
        "completed": False,
        "instructions": "Prepare complaint draft using Complaint Agent and submit to local station or online portal."
    })
    task_id += 1

    # 5. Document Recovery & DigiLocker
    for doc in structured_case.get("missing_documents", []):
        tasks.append({
            "id": task_id,
            "title": f"Access digital copy or apply for duplicate {doc}",
            "priority": "FOLLOW-UP",
            "category": "Document",
            "completed": False,
            "instructions": f"Use DigiLocker for instant digital access or apply on official portal for replacement {doc}."
        })
        task_id += 1

    return tasks