import json
import requests
from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from league.views import UpdateScoresView


class Command(BaseCommand):
    help = "Hourly job to update scores by calling UpdateScoresView"

    def add_arguments(self, parser):
        parser.add_argument(
            "--season",
            type=str,
            default="2025/26",
            help="Season to update scores for (default: 2025/26)"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Don't actually make the request, just show what would be done"
        )

    def handle(self, *args, **options):
        season = options["season"]
        dry_run = options["dry_run"]

        self.stdout.write(f"Starting hourly score update for season: {season}")
        
        if dry_run:
            self.stdout.write("DRY RUN - No actual requests will be made")
            return

        try:
            # Create a mock request to call the UpdateScoresView
            factory = RequestFactory()
            request = factory.post(
                "/update_scores/",
                data={"season": season},
                content_type="application/json"
            )
            request.user = AnonymousUser()

            # Call the view
            view = UpdateScoresView.as_view()
            response = view(request)

            if response.status_code == 200:
                response_data = response.data
                if response_data.get("status") == "skipped_recent_run":
                    self.stdout.write(
                        self.style.WARNING(
                            f"Update skipped - last run was within 24 hours"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully updated scores for season: {season}"
                        )
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Update failed with status code: {response.status_code}"
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error during hourly update: {str(e)}"
                )
            )
            raise
