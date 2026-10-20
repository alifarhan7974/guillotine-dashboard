
from guillotine import calculate_eliminations


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
