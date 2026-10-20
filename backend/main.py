
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

from sleeper_client import get_nfl_state, get_users, get_rosters, get_matchups, get_league as fetch_league
from guillotine import calculate_eliminations

app = FastAPI(title="Guillotine Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Guillotine Dashboard API is running"}


@app.get("/api/league/{league_id}")
async def get_league(league_id: str):
    try:
        league = await fetch_league(league_id)
        return {
            "league_id": league_id,
            "name": league.get("name"),
            "season": league.get("season"),
            "total_rosters": league.get("total_rosters"),
            "status": league.get("status"),
        }
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="League not found. Check the league ID.",
            )
        raise HTTPException(
            status_code=502,
            detail="Sleeper returned an error.",
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to Sleeper.",
        )


@app.get("/api/league/{league_id}/teams")
async def get_teams(league_id: str):
    try:
        users = await get_users(league_id)
        rosters = await get_rosters(league_id)

        # Map each Sleeper user ID to their display name.
        user_names = {
            user["user_id"]: user.get("display_name", "Unknown")
            for user in users
        }

        teams = []

        for roster in rosters:
            owner_id = roster.get("owner_id")

            teams.append({
                "roster_id": roster["roster_id"],
                "owner_name": user_names.get(owner_id, "Unknown"),
                "players": roster.get("players") or [],
            })

        return {"teams": teams}

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="League not found.")
        raise HTTPException(status_code=502, detail="Sleeper returned an error.")

    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Could not connect to Sleeper.")


@app.get("/api/league/{league_id}/matchups/{week}")
async def get_week_matchups(league_id: str, week: int):
    try:
        matchups = await get_matchups(league_id, week)

        return {
            "week": week,
            "matchups": [
                {
                    "roster_id": matchup["roster_id"],
                    "points": matchup.get("points", 0),
                    "matchup_id": matchup.get("matchup_id"),
                }
                for matchup in matchups
            ],
        }

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Sleeper returned HTTP {exc.response.status_code}.",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to Sleeper.",
        )

@app.get("/api/league/{league_id}/eliminations")
async def get_eliminations(league_id: str):
    try:
        # Fetch the teams and the current NFL week.
        users = await get_users(league_id)
        rosters = await get_rosters(league_id)
        nfl_state = await get_nfl_state()

        current_week = nfl_state.get("week")

        if not isinstance(current_week, int) or current_week < 1:
            raise HTTPException(
                status_code=502,
                detail="Could not determine the current NFL week.",
            )

        # Connect each roster to its owner's display name.
        user_names = {
            user["user_id"]: user.get("display_name", "Unknown")
            for user in users
        }

        teams = [
            {
                "roster_id": roster["roster_id"],
                "owner_name": user_names.get(
                    roster.get("owner_id"), "Unknown"
                ),
            }
            for roster in rosters
        ]

        # Collect scores from weeks before the current NFL week.
        weekly_scores = {}

        for week in range(1, current_week):
            matchups = await get_matchups(league_id, week)

            weekly_scores[week] = {
                matchup["roster_id"]: matchup.get("points", 0)
                for matchup in matchups
            }

        eliminations = calculate_eliminations(teams, weekly_scores)

        return {
            "league_id": league_id,
            "current_nfl_week": current_week,
            "eliminations": eliminations,
        }

    except HTTPException:
        raise

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="League or requested Sleeper resource not found.",
            )
        raise HTTPException(
            status_code=502,
            detail="Sleeper returned an error.",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to Sleeper.",
        )
