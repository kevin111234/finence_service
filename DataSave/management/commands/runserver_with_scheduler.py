from django.core.management.commands.runserver import Command as RunServerCommand
from threading import Thread
from finence_service.scheduler import start
from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as StaticRunServerCommand

class Command(StaticRunServerCommand):
    help = 'Starts the Django server and the APScheduler.'

    def inner_run(self, *args, **options):
        # 스케줄러를 별도의 스레드로 실행
        scheduler_thread = Thread(target=start)
        scheduler_thread.daemon = True
        scheduler_thread.start()

        # Django 서버 실행
        super().inner_run(*args, **options)