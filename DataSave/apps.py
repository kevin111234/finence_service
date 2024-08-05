from django.apps import AppConfig
import threading

class DataSaveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DataSave'

    def ready(self):
        from finence_service.scheduler import start
        scheduler_thread = threading.Thread(target=start)
        scheduler_thread.start()