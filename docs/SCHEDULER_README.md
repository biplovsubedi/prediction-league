# Score Update Scheduler (PythonAnywhere)

This document explains how to set up automated score updates using PythonAnywhere's scheduled tasks feature.

## Overview

The system automatically calls the `UpdateScoresView` once per day to:
- Update team data from FPL API
- Update gameweek information
- Update actual standings
- Compute and update scores for all players

**Note:** PythonAnywhere's free tier only supports daily tasks, not hourly. For more frequent updates, consider upgrading to a paid plan or using alternative solutions.

## PythonAnywhere Setup

### 1. Upload Scripts
Upload these scripts to your PythonAnywhere account:
- `scripts/pythonanywhere_daily_update.py` - Full version with logging
- `scripts/pythonanywhere_simple_update.py` - Simple version for testing

### 2. Configure Scheduled Task

1. Go to the **Tasks** tab in PythonAnywhere
2. Click **Add a new scheduled task**
3. Configure as follows:

**Frequency:** Daily  
**Time:** Choose your preferred time (e.g., 20:55 UTC for evening updates)  
**Command:** `python3 /home/yourusername/prediction-league/scripts/pythonanywhere_daily_update.py`  
**Description:** "Daily score update for prediction league"

**Note:** Replace `yourusername` with your actual PythonAnywhere username.

### 3. Test the Setup

Before setting up the scheduled task, test the script:

1. Go to **Consoles** tab in PythonAnywhere
2. Start a new console
3. Run: `python3 /home/yourusername/prediction-league/scripts/pythonanywhere_simple_update.py`

You should see output like:
```
Starting daily score update...
Note: This will respect the 24-hour debounce logic
Starting hourly score update for season: 2025/26
Update skipped - last run was within 24 hours
Daily score update completed successfully!
```

## Alternative Solutions for More Frequent Updates

### Option 1: PythonAnywhere Paid Plan
- **Hobbyist Plan**: Supports hourly tasks
- **Developer Plan**: Supports multiple hourly tasks
- **Professional Plan**: Full scheduling flexibility

### Option 2: External Cron Service
- **Cron-job.org**: Free hourly cron jobs
- **EasyCron**: Affordable hourly scheduling
- **SetCronJob**: Multiple free hourly jobs

### Option 3: Cloud Functions
- **AWS Lambda**: Serverless functions with CloudWatch Events
- **Google Cloud Functions**: Scheduled functions
- **Azure Functions**: Timer-triggered functions

## Management Commands

### Manual Updates
You can still run updates manually using Django management commands:

```bash
# Run for default season (2025/26)
python manage.py hourly_update_scores

# Run for specific season
python manage.py hourly_update_scores --season="2024/25"

# Dry run (no actual updates)
python manage.py hourly_update_scores --dry-run
```

### Scheduler Control (Local Development)
For local development, you can still use the scheduler:

```bash
# Start the scheduler
python manage.py control_scheduler start

# Check scheduler status
python manage.py control_scheduler status

# Stop the scheduler
python manage.py control_scheduler stop
```

## Monitoring

### PythonAnywhere Logs
- Check the **Tasks** tab for execution history
- View task output and any errors
- Monitor CPU usage and execution time

### Local Logs
- If using the full script: `logs/pythonanywhere_daily.log`
- Django logs for detailed application-level information

### Status Check
```bash
python manage.py hourly_update_scores --dry-run
```

## Configuration

### Season
The default season is "2025/26". Change this in:
- The PythonAnywhere script files
- Command line arguments for manual runs

### Update Frequency
- **Daily**: Default for PythonAnywhere free tier
- **Hourly**: Requires paid plan or external service
- **Custom**: Can be adjusted based on your needs and plan

## Troubleshooting

### Script Not Running
1. Check the command path in PythonAnywhere Tasks
2. Verify the script file exists and is executable
3. Test manually in the PythonAnywhere console

### Django Setup Issues
1. Ensure the project path is correct in the script
2. Check that Django settings module is accessible
3. Verify all required packages are installed

### API Issues
1. Check if FPL API is accessible from PythonAnywhere
2. Verify the 24-hour debounce logic isn't blocking updates
3. Check Django logs for detailed error messages

### Frequency Limitations
1. **Free Tier**: Only daily tasks supported
2. **Paid Plans**: Hourly and custom frequencies available
3. **External Services**: Alternative for hourly updates

## Advantages of PythonAnywhere Approach

- ✅ **Managed Infrastructure**: No server maintenance
- ✅ **Reliability**: 99.9% uptime guarantee
- ✅ **Easy Setup**: Simple web interface
- ✅ **Monitoring**: Execution history and logs
- ✅ **Resource Control**: CPU usage tracking
- ✅ **Console Access**: Easy testing and debugging

## Security Notes

- Scripts run with your PythonAnywhere permissions
- API calls are made to FPL's public endpoint
- No sensitive data is exposed
- The system respects the existing debounce logic in `UpdateScoresView`
