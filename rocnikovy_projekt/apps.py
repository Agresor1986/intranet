from django.apps import AppConfig

class MyProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rocnikovy_projekt"  # Názov tvojho hlavného projektu

    def ready(self):
        import rocnikovy_projekt.signals  # Načíta signály pri štarte projektu
