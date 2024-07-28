from django.apps import AppConfig

class a_backgroundConfig(AppConfig):
    name = 'a_background'

    def ready(self):
        pass