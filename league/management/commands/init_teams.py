import requests
from django.core.management.base import BaseCommand

from league.models import Team


FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


class Command(BaseCommand):
    help = "Fetch teams from FPL and upsert into DB"

    def handle(self, *args, **options):
        resp = requests.get(FPL_BOOTSTRAP_URL, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        count = 0
        for t in data.get("teams", []):
            Team.objects.update_or_create(
                id=t["id"],
                defaults={
                    "name": t.get("name", ""),
                    "short_name": t.get("short_name", ""),
                    "code": t.get("code", 0),
                },
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Upserted {count} teams"))


