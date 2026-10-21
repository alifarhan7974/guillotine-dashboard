
def calculate_weekly_views(teams: list, weekly_scores: dict) -> list:
    """Rank active teams and remove the lowest scorer each week.

    Tied weekly scores are resolved by the lower cumulative score through that
    week. Roster ID only keeps presentation deterministic if both tie.
    """
    alive = {team["roster_id"]: team for team in teams}
    cumulative_points = {team["roster_id"]: 0 for team in teams}
    views = []

    for week in sorted(weekly_scores):
        scores = weekly_scores[week]
        for roster_id, points in scores.items():
            if roster_id in cumulative_points:
                cumulative_points[roster_id] += points
        ranked_ids = sorted(
            (roster_id for roster_id in alive if roster_id in scores),
            key=lambda roster_id: (scores[roster_id], cumulative_points[roster_id], roster_id),
        )
        if not ranked_ids:
            continue

        final_team = len(ranked_ids) == 1
        standings = [
            {"rank": rank, "roster_id": roster_id, "owner_name": alive[roster_id]["owner_name"], "points": scores[roster_id], "cumulative_points": cumulative_points[roster_id], "status": "winner" if final_team else "eliminated" if rank == 1 else "safe"}
            for rank, roster_id in enumerate(ranked_ids, start=1)
        ]
        views.append({"week": week, "standings": standings, "eliminated": standings[0]})
        if final_team:
            break
        alive.pop(ranked_ids[0])
    return views


def calculate_eliminations(teams: list, weekly_scores: dict) -> list:
    return [
        {"week": view["week"], "roster_id": view["eliminated"]["roster_id"], "owner_name": view["eliminated"]["owner_name"], "points": view["eliminated"]["points"]}
        for view in calculate_weekly_views(teams, weekly_scores)
        if view["eliminated"]["status"] == "eliminated"
    ]
