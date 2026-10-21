from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from league_service import get_dashboard
from sleeper_client import SleeperClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.sleeper = SleeperClient()
    yield
    await app.state.sleeper.close()


app = FastAPI(title="Guillotine Dashboard API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Guillotine Dashboard API is running"}


@app.get("/api/league/{league_id}/dashboard")
async def league_dashboard(league_id: str, request: Request):
    try:
        return await get_dashboard(request.app.state.sleeper, league_id)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="League not found. Check the league ID.")
        raise HTTPException(status_code=502, detail="Sleeper returned an error.")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Could not connect to Sleeper.")
