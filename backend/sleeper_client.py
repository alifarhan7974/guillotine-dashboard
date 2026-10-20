
import httpx

BASE_URL = "https://api.sleeper.app/v1"


async def get_league(league_id: str) -> dict:
    url = f"{BASE_URL}/league/{league_id}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def get_users(league_id: str) -> list:
    url = f"{BASE_URL}/league/{league_id}/users"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def get_rosters(league_id: str) -> list:
    url = f"{BASE_URL}/league/{league_id}/rosters"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def get_matchups(league_id: str, week: int) -> list:
    url = f"{BASE_URL}/league/{league_id}/matchups/{week}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def get_nfl_state() -> dict:
    url = f"{BASE_URL}/state/nfl"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
