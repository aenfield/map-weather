from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('weather')

NWS_API_BASE = 'https://api.weather.gov'
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'application/geo+json'
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """Format an alert 'feature' from the NWS API into a human-readable string."""
    props = feature['properties']
    return f"""
Event:        {props.get('event', 'Unknown')}
Area:         {props.get('areaDesc', 'Unknown')}
Severity:     {props.get('severity', 'Unknown')}
Description:  {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

import asyncio

async def main():
    url = f"{NWS_API_BASE}/alerts/active/area/ID"
    print(url)
    resp = await make_nws_request(url)
    for feature in resp['features']:
        print(format_alert(feature))

if __name__ == '__main__':
    asyncio.run(main())