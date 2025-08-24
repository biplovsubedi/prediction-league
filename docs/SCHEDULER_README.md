# Score Update Scheduler

This document explains how to set up and use the automated score update scheduler that runs every hour.

## Overview

The scheduler automatically calls the `UpdateScoresView` every hour to:
- Update team data from FPL API
- Update gameweek information
- Update actual standings
- Compute and update scores for all players

## Components

### 1. Management Commands

#### `hourly_update_scores`
Runs the score update process manually:
```bash
# Run for default season (2025/26)
python manage.py hourly_update_scores

# Run for specific season
python manage.py hourly_update_scores --season="2024/25"

# Dry run (no actual updates)
python manage.py hourly_update_scores --dry-run
```

#### `control_scheduler`
Controls the background scheduler:
```bash
# Start the scheduler
python manage.py control_scheduler start

# Stop the scheduler
python manage.py control_scheduler stop

# Check scheduler status
python manage.py control_scheduler status
```

### 2. Automatic Scheduler

The scheduler automatically starts when Django starts and runs in the background. It:
- Runs every hour (configurable)
- Uses the `UpdateScoresView` logic
- Respects the 24-hour debounce (won't run if last update was within 24 hours)
- Logs all activities

## Setup Options

### Option 1: Automatic (Recommended)
The scheduler starts automatically when Django starts. No additional setup needed.

### Option 2: Manual Control
Use the management commands to control when the scheduler runs:
```bash
# Start the scheduler
python manage.py control_scheduler start

# Check if it's running
python manage.py control_scheduler status

# Stop when needed
python manage.py control_scheduler stop
```

### Option 3: Cron Job (Alternative)
If you prefer using system cron instead of the built-in scheduler:

1. Make the script executable:
```bash
chmod +x scripts/schedule_hourly_update.sh
```

2. Add to crontab (run `crontab -e`):
```bash
# Run every hour at minute 0
0 * * * * /Users/biplov/codebase/prediction-league/scripts/schedule_hourly_update.sh

# Or run every hour at minute 30
30 * * * * /Users/biplov/codebase/prediction-league/scripts/schedule_hourly_update.sh
```

## Monitoring

### Logs
- Scheduler activities are logged to Django's logging system
- Check Django logs for scheduler messages
- If using cron, logs are written to `logs/hourly_update.log`

### Status Check
```bash
python manage.py control_scheduler status
```

### Manual Test
```bash
python manage.py hourly_update_scores --dry-run
```

## Configuration

### Scheduler Interval
To change the interval, modify `league/scheduler.py`:
```python
class ScoreUpdateScheduler:
    def __init__(self, interval_hours=1):  # Change this value
```

### Season
The default season is "2025/26". Change this in:
- `league/scheduler.py` (for automatic scheduler)
- `scripts/schedule_hourly_update.sh` (for cron jobs)
- Command line arguments (for manual runs)

## Troubleshooting

### Scheduler Not Starting
1. Check Django logs for errors
2. Verify the app is properly configured in `INSTALLED_APPS`
3. Try starting manually: `python manage.py control_scheduler start`

### Updates Not Running
1. Check if last update was within 24 hours (debounce protection)
2. Verify FPL API is accessible
3. Check database connectivity

### Performance Issues
- The scheduler runs in a daemon thread and won't block Django
- Each update respects the 24-hour debounce to avoid unnecessary API calls
- Monitor logs for any long-running operations

## Security Notes

- The scheduler runs with Django's permissions
- API calls are made to FPL's public endpoint
- No sensitive data is exposed
- The scheduler respects the existing debounce logic in `UpdateScoresView`
