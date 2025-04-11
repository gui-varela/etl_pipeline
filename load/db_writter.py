import psycopg2
from psycopg2.extras import execute_values

# Configurações da conexão (ajuste conforme seu ambiente)
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "safabet",
    "user": "postgres",
    "password": "postgres"
}

TABLE_NAME = "fixtures"

def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            fixture_id   INTEGER PRIMARY KEY,
            date_utc     TIMESTAMP,
            venue_name   TEXT,
            venue_city   TEXT,
            status       TEXT,
            league_name  TEXT,
            league_round TEXT,
            home_team    TEXT,
            away_team    TEXT,
            goals_home   INTEGER,
            goals_away   INTEGER
        );
        """)
        conn.commit()

def insert_fixtures(conn, fixtures: list[dict]):
    if not fixtures:
        print("Nenhum dado para inserir.")
        return

    with conn.cursor() as cur:
        query = f"""
        INSERT INTO {TABLE_NAME} (
            fixture_id, date_utc, venue_name, venue_city, status,
            league_name, league_round, home_team, away_team,
            goals_home, goals_away
        ) VALUES %s
        ON CONFLICT (fixture_id) DO NOTHING;
        """

        values = [
            (
                f["fixture_id"],
                f["date"],
                f["venue_name"],
                f["venue_city"],
                f["status"],
                f["league_name"],
                f["league_round"],
                f["home_team"],
                f["away_team"],
                f["goals_home"],
                f["goals_away"],
            )
            for f in fixtures
        ]

        execute_values(cur, query, values)
        conn.commit()
        print(f"{len(values)} fixtures inseridos (ou já existentes).")

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
