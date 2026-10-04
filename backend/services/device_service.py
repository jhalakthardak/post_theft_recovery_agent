from backend.agents.device_recovery_agent import device_recovery_agent


def get_device_guidance(device_type: str) -> dict:
    return device_recovery_agent(device_type)