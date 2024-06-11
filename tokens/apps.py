from django.apps import AppConfig

class TokenFetcherConfig(AppConfig):
    name = 'tokens'

    def ready(self):
        from .updater import start_updater
        start_updater()