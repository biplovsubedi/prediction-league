"""
Utility functions for the prediction league system
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional

from .models import Team


def get_teams_lookup() -> Dict[int, Dict]:
    """
    Get a dictionary mapping team IDs to team information for quick lookup.
    
    Returns:
        Dict mapping team ID to team info dict with keys: id, name, short_name, code
    """
    teams = Team.objects.all().order_by('id')
    
    team_data = {}
    for team in teams:
        team_data[team.id] = {
            'id': team.id,
            'name': team.name,
            'short_name': team.short_name,
            'code': team.code
        }
    
    return team_data


def get_team_by_id(team_id: int) -> Optional[Dict]:
    """
    Get team information by ID.
    
    Args:
        team_id: The team ID to look up
        
    Returns:
        Team info dict or None if not found
    """
    try:
        team = Team.objects.get(id=team_id)
        return {
            'id': team.id,
            'name': team.name,
            'short_name': team.short_name,
            'code': team.code
        }
    except Team.DoesNotExist:
        return None


def get_team_by_name(team_name: str) -> Optional[Dict]:
    """
    Get team information by name (case-insensitive).
    
    Args:
        team_name: The team name to look up
        
    Returns:
        Team info dict or None if not found
    """
    try:
        team = Team.objects.filter(name__iexact=team_name).first()
        if team:
            return {
                'id': team.id,
                'name': team.name,
                'short_name': team.short_name,
                'code': team.code
            }
        return None
    except Exception:
        return None


def export_teams_to_json(output_path: str = "teams_lookup.json") -> str:
    """
    Export all teams to a JSON file for external use.
    
    Args:
        output_path: Path where to save the JSON file
        
    Returns:
        Path to the saved file
    """
    team_data = get_teams_lookup()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(team_data, f, indent=2, ensure_ascii=False)
    
    return output_path


def load_teams_from_json(json_path: str) -> Dict[int, Dict]:
    """
    Load team data from a JSON file.
    
    Args:
        json_path: Path to the JSON file
        
    Returns:
        Dict mapping team ID to team info
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
