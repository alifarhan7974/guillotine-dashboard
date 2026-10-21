import asyncio

from guillotine import calculate_weekly_views
from sleeper_client import SleeperClient

MAX_REGULAR_SEASON_WEEK = 18


async def get_dashboard(client: SleeperClient, league_id: str) -> dict:
    """Build a complete, week-by-week view that the UI can navigate locally."""
    league, users, rosters, nfl_state = await asyncio.gather(
        client.get_league(league_id), client.get_users(league_id),
        client.get_rosters(league_id), client.get_nfl_state(),
    )
    if str(nfl_state.get("season")) == str(league.get("season")):
        current_week = nfl_state.get("week", 1)
        current_week = current_week if isinstance(current_week, int) else 1
        max_week = min(MAX_REGULAR_SEASON_WEEK, max(0, current_week - 1))
    else:
        max_week = MAX_REGULAR_SEASON_WEEK

    matchup_lists = await asyncio.gather(*(client.get_matchups(league_id, week) for week in range(1, max_week + 1)))
    weekly_scores = {
        week: {matchup["roster_id"]: matchup.get("points", 0) for matchup in matchups}
        for week, matchups in enumerate(matchup_lists, start=1) if matchups
    }
    names = {user["user_id"]: user.get("display_name", "Unknown") for user in users}
    teams = [{"roster_id": roster["roster_id"], "owner_name": names.get(roster.get("owner_id"), "Unknown")} for roster in rosters]
    weeks = calculate_weekly_views(teams, weekly_scores)
    return {
        "league": {"league_id": league_id, "name": league.get("name"), "season": league.get("season"), "total_rosters": league.get("total_rosters"), "status": league.get("status")},
        "weeks": weeks, "available_weeks": [view["week"] for view in weeks],
        "latest_week": weeks[-1]["week"] if weeks else None,
    }
