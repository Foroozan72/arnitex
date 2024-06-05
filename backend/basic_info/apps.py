from django.apps import AppConfig

class BasicInfoConfig(AppConfig):
    name = 'basic_info'

    def ready(self):
        import basic_info.translation
