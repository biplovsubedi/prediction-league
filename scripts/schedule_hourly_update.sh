#!/bin/bash

# Script to run hourly score updates
# This should be added to crontab to run every hour

# Change to the project directory
cd /Users/biplov/codebase/prediction-league

# Activate virtual environment
source .venv/bin/activate

# Run the hourly update command
python manage.py hourly_update_scores --season="2025/26"

# Log the execution
echo "$(date): Hourly update completed" >> logs/hourly_update.log
