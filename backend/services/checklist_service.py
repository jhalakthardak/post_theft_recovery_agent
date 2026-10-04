def update_task_completion(checklist: list, task_id: int, completed: bool) -> list:
    for task in checklist:
        if task.get("id") == task_id:
            task["completed"] = completed
            break
    return checklist