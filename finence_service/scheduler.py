from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events

def scheduler_test():
    print("스케줄러 정상 작동중!")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 각 작업을 스케줄러에 추가하고 로그를 남깁니다.

    try:
# exchange_rate
    # 환율 데이터 저장 (오후 2시 마다)
        job = scheduler.add_job(scheduler_test, CronTrigger(minute="*/5"), id="test", replace_existing=True)
        print(f"Job {job.id} added to scheduler.")
        print("테스트 작업 등록 완료")

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