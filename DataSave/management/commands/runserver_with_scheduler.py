from django.core.management.commands.runserver import Command as RunServerCommand
from threading import Thread
from finence_service.scheduler import start
from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as StaticRunServerCommand
from DataSave.tasks import save_dollar_rate, save_dollar_index, save_stock_ticker, save_stock_data, save_stock_index, save_commodity_data

class Command(StaticRunServerCommand):
    help = 'Starts the Django server and the APScheduler.'

    def inner_run(self, *args, **options):
        # 스케줄러를 별도의 스레드로 실행
        scheduler_thread = Thread(target=self.start_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()

        # Django 서버 실행
        super().inner_run(*args, **options)
    
    def start_scheduler(self):
        start()
        
        # 초기 작업 실행
        self.run_initial_tasks()

    def run_initial_tasks(self):
        print("서버 시작 시 초기 작업을 실행합니다...")
        try:
            save_dollar_rate()
            save_dollar_index()
            save_stock_ticker()
            save_stock_data()
            save_stock_index()
            save_commodity_data()
            print("초기 작업 실행 완료.")
        except Exception as e:
            print(f"초기 작업 실행 중 오류 발생: {e}")