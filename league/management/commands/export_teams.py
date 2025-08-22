from django.core.management.base import BaseCommand
from league.utils import export_teams_to_json


class Command(BaseCommand):
    help = "Export all teams to JSON file for quick lookup"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output", 
            type=str, 
            default="teams_lookup.json",
            help="Output file path (default: teams_lookup.json)"
        )

    def handle(self, *args, **options):
        output_path = options["output"]
        
        try:
            file_path = export_teams_to_json(output_path)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully exported teams to {file_path}")
            )
            
            # Also show the team mapping
            from league.utils import get_teams_lookup
            teams = get_teams_lookup()
            
            self.stdout.write(f"\nExported {len(teams)} teams:")
            for team_id, team_info in teams.items():
                self.stdout.write(f"  {team_id}: {team_info['name']} ({team_info['short_name']})")
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to export teams: {e}")
            )
