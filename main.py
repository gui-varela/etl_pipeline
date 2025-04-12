import argparse
from transform.transformer import transform_fixtures
from load.db_writter import get_connection, create_table_if_not_exists, insert_fixtures
from extract.api_client import get_brasileirao_league_id, get_fixtures_for_week
from utils.logger import setup_logger
from utils.notifier import send_discord_alert
from config.settings import API_BASE_URL, API_KEY
from scheduler import start_scheduler

logger = setup_logger()

def run_etl():
    try:
        logger.info("🚀 Iniciando ETL do Brasileirão...")
        logger.info("🔎 Obtendo ID da liga e temporada atual...")
        league_id, season = get_brasileirao_league_id()

        logger.info("📅 Buscando partidas da semana...")
        raw_fixtures = get_fixtures_for_week(league_id, season)
        logger.info(f"✅ {len(raw_fixtures)} fixtures encontrados.")

        logger.info("🧪 Transformando dados brutos...")
        fixtures = transform_fixtures(raw_fixtures)

        logger.info("💾 Gravando dados no banco de dados...")
        with get_connection() as conn:
            create_table_if_not_exists(conn)
            insert_fixtures(conn, fixtures)

        logger.info("🎉 ETL concluído com sucesso!")
        send_discord_alert("Todos os dados foram processados e gravados com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro na execução do ETL: {e}")
        send_discord_alert(f"🚨 Falha na rotina ETL: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executa a rotina ETL ou inicia o agendador diário.")
    parser.add_argument("--schedule", action="store_true", help="Inicia o agendador diário.")
    args = parser.parse_args()

    if args.schedule:
        start_scheduler(run_etl, logger)
    else:
        run_etl()
