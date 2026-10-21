
import httpx


BASE_URL = "https://api.sleeper.app/v1"


class SleeperClient:
    """Small, reusable client for the Sleeper API."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url=BASE_URL, timeout=10.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str):
        response = await self._client.get(path)
        response.raise_for_status()
        return response.json()

    async def get_league(self, league_id: str) -> dict:
        return await self._get(f"/league/{league_id}")

    async def get_users(self, league_id: str) -> list:
        return await self._get(f"/league/{league_id}/users")

    async def get_rosters(self, league_id: str) -> list:
        return await self._get(f"/league/{league_id}/rosters")

    async def get_matchups(self, league_id: str, week: int) -> list:
        return await self._get(f"/league/{league_id}/matchups/{week}")

    async def get_nfl_state(self) -> dict:
        return await self._get("/state/nfl")
