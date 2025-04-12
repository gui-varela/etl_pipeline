import requests
from datetime import datetime, timedelta
from config.settings import API_BASE_URL, API_KEY

HEADERS = {
    "x-rapidapi-host": API_BASE_URL,
    "x-rapidapi-key": API_KEY
}

def get_brazil_leagues():
    url = f"{API_BASE_URL}/leagues"
    params = {"country": "Brazil"}

    response = requests.get(url, headers=HEADERS, params=params, verify=False)
    response.raise_for_status()

    leagues = response.json().get("response", [])
    return leagues

def get_brasileirao_league_id():
    leagues = get_brazil_leagues()
    for league in leagues:
        name = league["league"]["name"]
        if "brasileirão" in name.lower() or "serie a" in name.lower():
            return league["league"]["id"], league["seasons"][-1]["year"]  # pega o último ano disponível
    raise ValueError("Brasileirão não encontrado.")

def get_fixtures_for_week(league_id, season):
    today = datetime.utcnow().date()
    next_monday = today + timedelta(days=(0 - today.weekday()))
    next_sunday = next_monday + timedelta(days=13)

    params = {
        "league": league_id,
        "season": season,
        "from": next_monday.strftime("%Y-%m-%d"),
        "to": next_sunday.strftime("%Y-%m-%d")
    }

    url = f"{API_BASE_URL}/fixtures"
    response = requests.get(url, headers=HEADERS, params=params, verify=False)
    response.raise_for_status()

    return response.json().get("response", [])
