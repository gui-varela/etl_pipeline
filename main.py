from transform.transformer import transform_fixtures
from load.db_writter import get_connection, create_table_if_not_exists, insert_fixtures
from extract.api_client import get_brasileirao_league_id, get_fixtures_for_week
from utils.logger import setup_logger
from utils.notifier import send_discord_alert
from config.settings import API_BASE_URL, API_KEY

required_vars = [API_BASE_URL, API_KEY]
for var in required_vars:
    if not var:
        raise EnvironmentError(f"Variável de ambiente obrigatória não definida: {var}")

logger = setup_logger()

def main():
    try:
        logger.info("🚀 Iniciando ETL do Brasileirão...")

        logger.info("🔍 Obtendo ID da liga e temporada atual...")
        league_id, season = get_brasileirao_league_id()

        logger.info("📅 Buscando partidas da semana...")
        raw_fixtures = get_fixtures_for_week(league_id, season)
        logger.info(f"✅ {len(raw_fixtures)} fixtures encontrados.")

        logger.info("🛠️ Transformando dados brutos...")
        fixtures = transform_fixtures(raw_fixtures)

        logger.info("💾 Gravando dados no banco...")
        with get_connection() as conn:
            create_table_if_not_exists(conn)
            insert_fixtures(conn, fixtures)

        logger.info("🎯 Processo concluído com sucesso.")
        send_discord_alert("Todos os dados foram processados e gravados com sucesso!")
    except Exception as e:
        logger.exception("❌ Erro durante o processo ETL:")
        send_discord_alert("Houve uma falha durante o processo de ETL. Verifique os logs. 🚨", success=False)
        raise e

if __name__ == "__main__":
    main()
