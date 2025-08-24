#!/usr/bin/env python3
"""
PythonAnywhere Daily Scheduled Task Script for Score Updates

This script is designed to be run as a PythonAnywhere scheduled task.
It will update scores by calling the UpdateScoresView once per day.

To set up:
1. Upload this script to your PythonAnywhere account
2. Go to Tasks tab in PythonAnywhere
3. Set frequency to "Daily"
4. Set command to: python3 /home/yourusername/prediction-league/scripts/pythonanywhere_daily_update.py
5. Set description: "Daily score update for prediction league"

Note: PythonAnywhere free tier only supports daily tasks, not hourly.
"""

import os
import sys
import django
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/yourusername/prediction-league/logs/pythonanywhere_daily.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def setup_django():
    """Set up Django environment"""
    try:
        # Add the project root to Python path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plsite.settings')
        django.setup()
        
        logger.info("Django environment set up successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to set up Django environment: {e}")
        return False

def run_daily_update():
    """Run the daily score update"""
    try:
        from django.core.management import call_command
        
        logger.info("Starting daily score update...")
        
        # Call the hourly update command (it will respect the 24-hour debounce)
        call_command('hourly_update_scores', verbosity=0)
        
        logger.info("Daily score update completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during daily update: {e}")
        return False

def main():
    """Main function"""
    start_time = datetime.now()
    logger.info(f"Starting PythonAnywhere daily update script at {start_time}")
    
    # Set up Django
    if not setup_django():
        logger.error("Failed to set up Django - exiting")
        sys.exit(1)
    
    # Run the update
    success = run_daily_update()
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    if success:
        logger.info(f"Script completed successfully in {duration}")
    else:
        logger.error(f"Script failed after {duration}")
        sys.exit(1)

if __name__ == '__main__':
    main()
