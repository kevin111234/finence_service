from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from a_coin_analyze.tasks import crawling_coin
from a_exchange_rate.tasks import crawling_exchange, slack_exchange, crawling_index
from a_stock_analyze.tasks import stock_ticker_save, stock_data_save, stock_index_save

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 각 작업을 스케줄러에 추가하고 로그를 남깁니다.

    try:
# exchange_rate
    # 환율 데이터 저장 (오후 2시 마다)
        job = scheduler.add_job(crawling_exchange, CronTrigger(hour=14, minute=0), id="exchange_crawling", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("exchange rate 크롤링 작업 등록 완료")

    # 달러 인덱스 데이터 저장 (30분 마다)
        job = scheduler.add_job(crawling_index, CronTrigger(minute="*/30"), id="index_crawling", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("dollar index 크롤링 작업 등록 완료")

    # Slack 환율정보 알림 (30분 마다)
        job = scheduler.add_job(slack_exchange, CronTrigger(minute="*/30"), id="slack_notice", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("slack 알림 작업 등록 완료")

# stock_analyze
    # 주식 티커 저장 (오후 3시 30분 마다)
        job = scheduler.add_job(stock_ticker_save, CronTrigger(hour=15, minute=30), id="stock_ticker_save", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("stock ticker 크롤링 작업 등록 완료")

    # 주가 데이터 저장 (오후 4시 마다)
        job = scheduler.add_job(stock_data_save, CronTrigger(hour=16, minute=0), id="stock_data_save", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("stock data 크롤링 작업 등록 완료")

    # 시장 지표 데이터 저장 (오후 4시 마다)
        job = scheduler.add_job(stock_index_save, CronTrigger(hour=16, minute=0), id="stock_index_save", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("index 데이터 저장 작업 등록 완료")

    # 원자재 데이터 저장 (오후 4시 마다)
    # 재무제표 데이터 저장 (오후 5시 마다)


    except Exception as e:
        print(f"Error adding job stock_crawling: {e}")


    # 이벤트 등록
    register_events(scheduler)

    # 스케줄러 시작
    scheduler.start()
    print("스케줄러 실행 성공!")

    # 작업이 올바르게 등록되었는지 확인
    if job:
        print(f"Job {job.id} added to scheduler.")
    else:
        print("Job was not added to scheduler.")
