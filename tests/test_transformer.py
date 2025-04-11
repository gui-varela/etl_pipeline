from transform.transformer import transform_fixtures
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

mock_raw_fixtures = [
    {
        "fixture": {
            "id": 123,
            "date": "2025-04-13T19:00:00+00:00"
        },
        "league": {
            "id": 71,
            "name": "Brasileirão",
            "season": 2025
        },
        "teams": {
            "home": {"id": 1, "name": "Time A"},
            "away": {"id": 2, "name": "Time B"}
        },
        "goals": {"home": 2, "away": 1},
        "score": {
            "halftime": {"home": 1, "away": 1},
            "fulltime": {"home": 2, "away": 1}
        }
    }
]

def test_transform_fixtures_basic():
    result = transform_fixtures(mock_raw_fixtures)

    assert len(result) == 1

    fixture = result[0]
    assert fixture["fixture_id"] == 123
    assert fixture["date"] == "2025-04-13T19:00:00+00:00"
    assert fixture["league_id"] == 71
    assert fixture["league_name"] == "Brasileirão"
    assert fixture["season"] == 2025
    assert fixture["home_team"] == "Time A"
    assert fixture["away_team"] == "Time B"
    assert fixture["goals_home"] == 2
    assert fixture["goals_away"] == 1
