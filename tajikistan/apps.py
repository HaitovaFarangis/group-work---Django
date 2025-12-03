from django.apps import AppConfig


class TajikistanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tajikistan'
    def ready(self):
        import tajikistan.signals