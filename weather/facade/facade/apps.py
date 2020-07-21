from django.apps import AppConfig


class FacadeConfig(AppConfig):
    name = 'facade'

    def ready(self):
        import facade.signals
