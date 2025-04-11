from apscheduler.schedulers.blocking import BlockingScheduler
from main import main

def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', hour=0, minute=0)
    
    print("Scheduler iniciado. ETL será executado diariamente à meia-noite.")
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()