from django.apps import AppConfig


class LeagueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "league"

    # Removed automatic scheduler startup - will use PythonAnywhere scheduled tasks instead
