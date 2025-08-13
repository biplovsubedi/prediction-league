import requests
from django.core.management.base import BaseCommand

from league.models import Gameweek


FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


class Command(BaseCommand):
    help = "Fetch events from FPL and upsert Gameweek rows"

    def handle(self, *args, **options):
        resp = requests.get(FPL_BOOTSTRAP_URL, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        count = 0
        for ev in data.get("events", []):
            Gameweek.objects.update_or_create(
                id=ev["id"],
                defaults={
                    "is_current": ev.get("is_current", False),
                    "finished": ev.get("finished", False),
                    "data_checked": ev.get("data_checked", False),
                },
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Upserted {count} gameweeks"))


