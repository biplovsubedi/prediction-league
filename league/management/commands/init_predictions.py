import csv
from pathlib import Path
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError

from league.models import Player, Prediction, Team


class Command(BaseCommand):
    help = (
        "Initialize predictions from a CSV file: "
        "user_name,team_name,predicted_1,...,predicted_20,player_type"
    )

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)
        parser.add_argument("--season", type=str, default="2025/26")

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"]).expanduser()
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        season: str = options["season"]
        created_players = 0
        created_predictions = 0

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0].startswith("#"):
                    continue
                if len(row) < 23:
                    raise CommandError("Row does not have 23 columns (got %d): %s" % (len(row), row))
                username = row[0].strip()
                team_name = row[1].strip()
                predicted_ranks = [int(x.strip()) for x in row[2:22]]
                player_type = row[22].strip() or "normal"

                # Ensure player
                player, created = Player.objects.get_or_create(
                    username=username,
                    defaults={"player_type": player_type},
                )
                if created:
                    created_players += 1

                # Resolve favourite team if present
                fav = Team.objects.filter(name__iexact=team_name).first()
                if fav and player.favourite_team_id != fav.id:
                    player.favourite_team = fav
                    player.save(update_fields=["favourite_team"])

                # We expect predicted_ranks[i] gives standing for team (i+1) by team id
                # But the planning doc says predicted_n contains the predicted rank for each team.
                # We will map by team id 1..20 in order of FPL ids.
                teams = list(Team.objects.order_by("id"))
                if len(teams) < 20:
                    raise CommandError("Expected at least 20 teams in DB. Run init_teams first.")
                for idx, team in enumerate(teams[:20]):
                    rank = predicted_ranks[idx]
                    Prediction.objects.update_or_create(
                        season=season,
                        player=player,
                        team=team,
                        defaults={"predicted_rank": rank},
                    )
                    created_predictions += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Processed predictions. players={created_players}, predictions={created_predictions}"
            )
        )


