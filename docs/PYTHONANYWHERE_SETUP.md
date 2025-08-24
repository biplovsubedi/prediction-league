# PythonAnywhere Quick Setup Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Upload Scripts
Upload these files to your PythonAnywhere account:
- `scripts/pythonanywhere_daily_update.py` - Full version with logging
- `scripts/pythonanywhere_simple_update.py` - Simple version for testing

### Step 2: Test the Script
1. Go to **Consoles** tab
2. Start a new console
3. Run: `python3 /home/yourusername/prediction-league/scripts/pythonanywhere_simple_update.py`
4. You should see: "Daily score update completed successfully!"

### Step 3: Set Up Scheduled Task
1. Go to **Tasks** tab
2. Click **Add a new scheduled task**
3. Fill in:
   - **Frequency**: Daily
   - **Time**: 20:55 UTC (or your preferred time)
   - **Command**: `python3 /home/yourusername/prediction-league/scripts/pythonanywhere_daily_update.py`
   - **Description**: "Daily score update"

**Note:** PythonAnywhere free tier only supports daily tasks, not hourly.

### Step 4: Verify
- Check **Tasks** tab for execution history
- Monitor CPU usage
- Check logs in `logs/pythonanywhere_daily.log`

## 📁 File Structure
```
/home/yourusername/prediction-league/
├── scripts/
│   ├── pythonanywhere_daily_update.py     # Full version with logging
│   └── pythonanywhere_simple_update.py   # Simple version for testing
├── logs/
│   └── pythonanywhere_daily.log          # Execution logs
└── ... (rest of your Django project)
```

## 🔧 Customization

### Change Season
Edit the script files and change:
```python
call_command('hourly_update_scores', '--season', '2024/25', verbosity=0)
```

### Change Frequency
In PythonAnywhere Tasks:
- **Daily**: Once per day (free tier)
- **Hourly**: Requires paid plan
- **Custom**: Available on paid plans

### Change Logging
Edit `pythonanywhere_daily_update.py` to modify log levels or file paths.

## 🚀 Getting Hourly Updates

Since PythonAnywhere free tier only supports daily tasks, here are alternatives for hourly updates:

### Option 1: Upgrade PythonAnywhere
- **Hobbyist Plan** ($5/month): Hourly tasks
- **Developer Plan** ($12/month): Multiple hourly tasks

### Option 2: Free External Services
- **Cron-job.org**: Free hourly cron jobs
- **EasyCron**: Affordable hourly scheduling
- **SetCronJob**: Multiple free hourly jobs

### Option 3: Cloud Functions
- **AWS Lambda**: Serverless with CloudWatch Events
- **Google Cloud Functions**: Scheduled functions
- **Azure Functions**: Timer-triggered functions

## 🐛 Troubleshooting

### Script Won't Run
- Check file paths in PythonAnywhere
- Verify Python version (use `python3`)
- Test manually in console first

### Django Import Errors
- Ensure project path is correct in script
- Check `DJANGO_SETTINGS_MODULE` is set
- Verify all packages are installed

### API Issues
- Check if FPL API is accessible
- Verify 24-hour debounce isn't blocking
- Check Django logs for details

### Frequency Limitations
- **Free Tier**: Only daily tasks supported
- **Paid Plans**: Hourly and custom frequencies available
- **External Services**: Alternative for hourly updates

## 📊 Monitoring

### PythonAnywhere Dashboard
- **Tasks**: Execution history and status
- **CPU**: Usage tracking and limits
- **Console**: Manual testing and debugging

### Logs
- **Application**: Django logs for detailed info
- **Script**: `logs/pythonanywhere_daily.log` for execution details
- **Tasks**: PythonAnywhere task output

## ✅ Benefits

- **Managed Infrastructure**: No server maintenance
- **Better Monitoring**: Full execution history
- **Resource Control**: CPU usage tracking
- **Easy Debugging**: Console access
- **Flexible Scheduling**: Adjust frequency easily
- **Reliable**: 99.9% uptime guarantee

## 🔒 Security

- Scripts run with your account permissions
- No sensitive data exposed
- FPL API calls are public
- Respects existing debounce logic

## 💡 Recommendations

### For Free Tier Users
- **Daily updates** are sufficient for most use cases
- **Manual updates** when needed using Django commands
- **Monitor execution** through PythonAnywhere dashboard

### For Paid Users
- **Upgrade to Hobbyist** for hourly updates
- **Multiple tasks** for different seasons
- **Custom scheduling** for optimal timing

### For Power Users
- **External cron services** for hourly updates
- **Cloud functions** for enterprise solutions
- **Hybrid approach** combining multiple services
