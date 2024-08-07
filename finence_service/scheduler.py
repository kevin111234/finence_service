from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from DataSave.tasks import save_dollar_rate, save_dollar_index, save_stock_ticker, save_stock_data, save_stock_index, save_commodity_data

def scheduler_test():
    print("스케줄러 정상 작동중!")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 각 작업을 스케줄러에 추가하고 로그를 남깁니다.

    try:
        job_defaults = {
            'coalesce': False,  # Do not merge missed jobs
            'max_instances': 3  # Allow up to 3 instances of the job
        }
        scheduler.configure(job_defaults=job_defaults)

        job = scheduler.add_job(scheduler_test, CronTrigger(minute="*/5"), id="test", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("테스트 작업 등록 완료")

# exchange_rate
        job = scheduler.add_job(save_dollar_rate, CronTrigger(hour=14, minute=0), id="exchange_rate", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("환율 저장 작업 등록 완료")

        job = scheduler.add_job(save_dollar_index, CronTrigger(hour=14, minute=0), id="dollar_index", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("달러 인덱스 저장 작업 등록 완료")

# stock_data
        job = scheduler.add_job(save_stock_ticker, CronTrigger(hour=15, minute=0), id="stock_ticker", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("미장 티커 저장 작업 등록 완료")

        job = scheduler.add_job(save_stock_data, CronTrigger(hour=16, minute=0), id="stock_data", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("미장 주가정보 저장 작업 등록 완료")

        job = scheduler.add_job(save_stock_index, CronTrigger(hour=16, minute=0), id="stock_index", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("시장지표 저장 작업 등록 완료")

        job = scheduler.add_job(save_commodity_data, CronTrigger(hour=16, minute=0), id="commodity_data", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("원자재 데이터 저장 작업 등록 완료")

    except Exception as e:
        print(f"Error adding job: {e}")


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