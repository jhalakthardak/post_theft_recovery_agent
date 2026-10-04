def replanning_agent(existing_checklist: list, new_information: dict) -> list:
    """
    Dynamically updates recovery plan when situation changes.
    """
    updated_list = list(existing_checklist)
    next_id = max([item["id"] for item in updated_list], default=0) + 1

    new_docs = new_information.get("additional_documents", [])
    for doc in new_docs:
        updated_list.append({
            "id": next_id,
            "title": f"Access digital copy or apply for duplicate {doc}",
            "priority": "FOLLOW-UP",
            "category": "Document",
            "completed": False,
            "instructions": f"Updated recovery step added for {doc}."
        })
        next_id += 1

    return updated_list