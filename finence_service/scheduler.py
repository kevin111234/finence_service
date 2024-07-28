from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
import logging
from a_coin_analyze.tasks import crawling_coin
from a_exchange_rate.tasks import crawling_exchange
from a_stock_analyze.tasks import crawling_stock

logger = logging.getLogger(__name__)

def my_scheduled_task():
    print("스케줄된 작업을 수행합니다")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    job = scheduler.add_job(my_scheduled_task, CronTrigger(minute="*/5"), id="my_scheduled_task", replace_existing=True)
    job = scheduler.add_job(crawling_coin, CronTrigger(minute="*/5"), id="my_scheduled_task", replace_existing=True)
    job = scheduler.add_job(crawling_exchange, CronTrigger(minute="*/5"), id="my_scheduled_task", replace_existing=True)
    job = scheduler.add_job(crawling_stock, CronTrigger(minute="*/5"), id="my_scheduled_task", replace_existing=True)

    register_events(scheduler)
    scheduler.start()
    logger.info("Scheduler started...")
    print("스케줄러 실행 성공!")

    # 작업이 올바르게 등록되었는지 확인
    if job:
        logger.info(f"Job {job.id} added to scheduler.")
    else:
        logger.error("Job was not added to scheduler.")
