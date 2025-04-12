# scheduler.py

import schedule
import time

def start_scheduler(job_function, logger, schedule_time="08:00"):
    schedule.every(1).minutes.do(job_function)
    logger.info(f"⏰ Agendador iniciado. Aguardando a próxima execução diária às {schedule_time}.")
    while True:
        schedule.run_pending()
        time.sleep(1)
