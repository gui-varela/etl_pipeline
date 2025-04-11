# utils/notifier.py
import requests
from config.settings import DISCORD_WEBHOOK_URL

def send_discord_alert(message: str, success: bool = True):
    if not DISCORD_WEBHOOK_URL:
        return

    emoji = "✅" if success else "❌"
    title = f"{emoji} ETL do Brasileirão {'concluído' if success else 'falhou'}"

    payload = {
        "content": f"**{title}**\n{message}"
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10, verify=False)
    except Exception as e:
        print(f"Erro ao enviar alerta ao Discord: {e}")
