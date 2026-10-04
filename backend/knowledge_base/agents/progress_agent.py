def progress_agent(checklist: list) -> dict:
    """
    Calculates completion percentage and pending status.
    """
    if not checklist:
        return {"total": 0, "completed": 0, "percentage": 0.0}

    total = len(checklist)
    completed = sum(1 for item in checklist if item.get("completed", False))
    percentage = round((completed / total) * 100, 1)

    return {
        "total": total,
        "completed": completed,
        "percentage": percentage
    }