import csv
from pathlib import Path
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError

from league.models import Player, Prediction, Team
from league.utils import get_teams_lookup


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
                team_name = row[1].strip()  # This is the user's prediction alias/entry name
                predicted_ranks = [int(x.strip()) for x in row[2:22]]
                player_type = row[22].strip() or "normal"

                # Ensure player
                player, created = Player.objects.get_or_create(
                    username=username,
                    defaults={"player_type": player_type, "custom_team_name": team_name},
                )
                if created:
                    created_players += 1
                else:
                    # Update custom_team_name if it changed
                    if player.custom_team_name != team_name:
                        player.custom_team_name = team_name
                        player.save(update_fields=["custom_team_name"])

                # The CSV contains: predicted_ranks[i] = team ID that should be in position (i+1)
                # So predicted_ranks[0] = team ID for 1st place, predicted_ranks[1] = team ID for 2nd place, etc.
                teams_lookup = get_teams_lookup()
                if len(teams_lookup) < 20:
                    raise CommandError("Expected at least 20 teams in DB. Run init_teams first.")
                
                # Create predictions for each rank position
                for rank_position in range(1, 21):  # Ranks 1-20
                    team_id = predicted_ranks[rank_position - 1]  # Get team ID for this rank position
                    
                    if team_id == 0:
                        self.stdout.write(f"Warning: User {username} has no prediction for rank {rank_position}")
                        continue
                        
                    if team_id not in teams_lookup:
                        raise CommandError(f"Team ID {team_id} not found in database for user {username}")
                    
                    team = Team.objects.get(id=team_id)
                    
                    Prediction.objects.update_or_create(
                        season=season,
                        player=player,
                        team=team,
                        defaults={"predicted_rank": rank_position},
                    )
                    created_predictions += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Processed predictions. players={created_players}, predictions={created_predictions}"
            )
        )


