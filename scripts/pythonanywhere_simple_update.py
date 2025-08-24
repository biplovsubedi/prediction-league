#!/usr/bin/env python3
"""
Simple PythonAnywhere Daily Score Update Script

This script can be run directly from the PythonAnywhere console or as a scheduled task.
It's simpler and more direct than the full version.

Note: PythonAnywhere free tier only supports daily tasks, not hourly.

Usage:
1. From console: python3 /home/yourusername/prediction-league/scripts/pythonanywhere_simple_update.py
2. As scheduled task: Set command to this script path with "Daily" frequency
"""

import os
import sys
import django
from pathlib import Path

# Add project to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plsite.settings')
django.setup()

# Now run the update
from django.core.management import call_command

print("Starting daily score update...")
print("Note: This will respect the 24-hour debounce logic")
try:
    call_command('hourly_update_scores', verbosity=1)
    print("Daily score update completed successfully!")
except Exception as e:
    print(f"Error during score update: {e}")
    sys.exit(1)
