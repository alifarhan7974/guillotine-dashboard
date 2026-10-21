
from guillotine import calculate_eliminations, calculate_weekly_views


def test_calculate_eliminations():
    teams = [
        {"roster_id": 1, "owner_name": "Alice"},
        {"roster_id": 2, "owner_name": "Bob"},
        {"roster_id": 3, "owner_name": "Charlie"},
    ]

    weekly_scores = {
        1: {1: 80.0, 2: 100.0, 3: 90.0},
        2: {2: 85.0, 3: 95.0},
    }

    result = calculate_eliminations(teams, weekly_scores)

    assert result == [
        {
            "week": 1,
            "roster_id": 1,
            "owner_name": "Alice",
            "points": 80.0,
        },
        {
            "week": 2,
            "roster_id": 2,
            "owner_name": "Bob",
            "points": 85.0,
        },
    ]


def test_tie_uses_cumulative_points():
    teams = [
        {"roster_id": 1, "owner_name": "Alice"},
        {"roster_id": 2, "owner_name": "Bob"},
        {"roster_id": 3, "owner_name": "Charlie"},
    ]
    weekly_scores = {
        1: {1: 80.0, 2: 100.0, 3: 90.0},
        2: {2: 85.0, 3: 85.0},
    }

    result = calculate_eliminations(teams, weekly_scores)

    # Both remaining teams score 85 in week 2, but Charlie has fewer
    # cumulative points through that week (175 versus Bob's 185).
    assert result[1]["roster_id"] == 3


def test_last_remaining_team_is_a_winner():
    teams = [{"roster_id": 1, "owner_name": "Alice"}, {"roster_id": 2, "owner_name": "Bob"}]
    views = calculate_weekly_views(teams, {1: {1: 80.0, 2: 100.0}, 2: {2: 90.0}})

    assert views[-1]["eliminated"]["status"] == "winner"
