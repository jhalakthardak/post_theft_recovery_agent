import urllib.parse

def police_routing_agent(location: str) -> dict:
    """
    Identifies nearby police reporting channels using incident location.
    """
    if not location or not location.strip():
        location = "current location"

    query = urllib.parse.quote(f"police station near {location}")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"

    return {
        "location": location,
        "guidance": "Use official police portals or present the generated draft at your local jurisdiction station.",
        "maps_url": maps_url
    }