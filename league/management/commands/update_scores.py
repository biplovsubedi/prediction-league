from django.core.management.base import BaseCommand
from django.test import RequestFactory

from league.views import UpdateScoresView


class Command(BaseCommand):
    help = "Invoke the update_scores API logic from CLI"

    def add_arguments(self, parser):
        parser.add_argument("--season", type=str, default="2025/26")

    def handle(self, *args, **options):
        rf = RequestFactory()
        request = rf.post("/api/update_scores/", data={"season": options["season"]})
        response = UpdateScoresView.as_view()(request)
        self.stdout.write(self.style.SUCCESS(f"Status: {response.data}"))


