from django.core.management.base import BaseCommand
from league.scheduler import start_scheduler, stop_scheduler, is_scheduler_running


class Command(BaseCommand):
    help = "Control the score update scheduler"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["start", "stop", "status"],
            help="Action to perform: start, stop, or check status"
        )

    def handle(self, *args, **options):
        action = options["action"]
        
        if action == "start":
            if is_scheduler_running():
                self.stdout.write(
                    self.style.WARNING("Scheduler is already running")
                )
            else:
                start_scheduler()
                self.stdout.write(
                    self.style.SUCCESS("Scheduler started successfully")
                )
                
        elif action == "stop":
            if not is_scheduler_running():
                self.stdout.write(
                    self.style.WARNING("Scheduler is not running")
                )
            else:
                stop_scheduler()
                self.stdout.write(
                    self.style.SUCCESS("Scheduler stopped successfully")
                )
                
        elif action == "status":
            if is_scheduler_running():
                self.stdout.write(
                    self.style.SUCCESS("Scheduler is RUNNING")
                )
            else:
                self.stdout.write(
                    self.style.ERROR("Scheduler is STOPPED")
                )
