from backend.agents.police_routing_agent import police_routing_agent


def get_police_routing(location: str) -> dict:
    return police_routing_agent(location)