
def calculate_eliminations(teams: list, weekly_scores: dict) -> list:
    # Start with every roster alive.
    alive = {
        team["roster_id"]: team
        for team in teams
    }

    eliminations = []

    # Process weeks in chronological order.
    for week in sorted(weekly_scores):
        scores = weekly_scores[week]

        # Only consider teams that are still alive and have a score.
        candidates = [
            (roster_id, scores[roster_id])
            for roster_id in alive
            if roster_id in scores
        ]

        # Skip a week if there are no scores to compare.
        if not candidates:
            continue

        # Find the lowest-scoring surviving team.
        eliminated_id, lowest_score = min(
            candidates,
            key=lambda candidate: candidate[1],
        )

        eliminated_team = alive.pop(eliminated_id)

        eliminations.append({
            "week": week,
            "roster_id": eliminated_id,
            "owner_name": eliminated_team["owner_name"],
            "points": lowest_score,
        })

    return eliminations
