from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
import logging
from a_coin_analyze.tasks import crawling_coin
from a_exchange_rate.tasks import crawling_exchange, slack_exchange
from a_stock_analyze.tasks import crawling_stock

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 각 작업을 스케줄러에 추가하고 로그를 남깁니다.

    try:
        job = scheduler.add_job(crawling_coin, CronTrigger(minute="*/30"), id="coin_crawling", replace_existing=True)
        logger.info(f"Job {job.id} added to scheduler.")
    except Exception as e:
        logger.error(f"Error adding job coin_crawling: {e}")

    # 환율, 달러 인덱스 데이터 크롤링 (20분마다)
    try:
        job = scheduler.add_job(crawling_exchange, CronTrigger(minute="*/20"), id="exchange_crawling", replace_existing=True)
        logger.info(f"Job {job.id} added to scheduler.")
    except Exception as e:
        logger.error(f"Error adding job exchange_crawling: {e}")

    # Slack 환율정보 알림 (30분마다)
    try:
        job = scheduler.add_job(slack_exchange, CronTrigger(minute="*/30"), id="exchange_crawling", replace_existing=True)
        logger.info(f"Job {job.id} added to scheduler.")
    except Exception as e:
        logger.error(f"Error adding job exchange_crawling: {e}")

    try:
        job = scheduler.add_job(crawling_stock, CronTrigger(minute="*/30"), id="stock_crawling", replace_existing=True)
        logger.info(f"Job {job.id} added to scheduler.")
    except Exception as e:
        logger.error(f"Error adding job stock_crawling: {e}")

    # 이벤트 등록
    register_events(scheduler)

    # 스케줄러 시작
    scheduler.start()
    logger.info("Scheduler started...")
    print("스케줄러 실행 성공!")

    # 작업이 올바르게 등록되었는지 확인
    if job:
        logger.info(f"Job {job.id} added to scheduler.")
    else:
        logger.error("Job was not added to scheduler.")
