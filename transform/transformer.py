from datetime import datetime

def transform_fixture(raw_fixture: dict) -> dict:
    fixture = raw_fixture.get("fixture", {})
    league = raw_fixture.get("league", {})
    teams = raw_fixture.get("teams", {})
    goals = raw_fixture.get("goals", {})

    return {
        "fixture_id": fixture.get("id"),
        "date": fixture.get("date"),
        "venue_name": fixture.get("venue", {}).get("name"),
        "venue_city": fixture.get("venue", {}).get("city"),
        "status": fixture.get("status", {}).get("short"),

        "league_id": league.get("id"),
        "season": league.get("season"),
        "league_name": league.get("name"),
        "league_round": league.get("round"),

        "home_team": teams.get("home", {}).get("name"),
        "away_team": teams.get("away", {}).get("name"),

        "goals_home": goals.get("home"),
        "goals_away": goals.get("away"),
    }

def transform_fixtures(raw_fixtures: list[dict]) -> list[dict]:
    return [transform_fixture(f) for f in raw_fixtures]
