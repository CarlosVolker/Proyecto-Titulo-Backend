from django.apps import AppConfig


class ApipoligonoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apipoligono'
    
    def ready(self):
        import apipoligono.signals
