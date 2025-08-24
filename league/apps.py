from django.apps import AppConfig


class LeagueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "league"

    def ready(self):
        """Called when Django starts"""
        # Import and start the scheduler only when Django is fully loaded
        # This prevents running during management commands
        import os
        if os.environ.get('RUN_MAIN') or os.environ.get('DJANGO_SETTINGS_MODULE'):
            try:
                from .scheduler import start_scheduler
                start_scheduler()
            except Exception as e:
                # Log error but don't crash the app
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to start scheduler: {e}")
