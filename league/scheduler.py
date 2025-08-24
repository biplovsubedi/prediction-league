"""
Scheduler module for running periodic tasks within Django
"""
import threading
import time
import logging
from datetime import datetime, timedelta
from django.core.management import call_command
from django.conf import settings

logger = logging.getLogger(__name__)


class ScoreUpdateScheduler:
    """Scheduler for running score updates every hour"""
    
    def __init__(self, interval_hours=1):
        self.interval_hours = interval_hours
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the scheduler in a background thread"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info(f"Score update scheduler started (every {self.interval_hours} hour(s))")
        
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Score update scheduler stopped")
        
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                # Run the hourly update command
                logger.info("Running scheduled score update...")
                call_command('hourly_update_scores', verbosity=0)
                logger.info("Scheduled score update completed")
                
            except Exception as e:
                logger.error(f"Error in scheduled score update: {e}")
                
            # Wait for the next interval
            time.sleep(self.interval_hours * 3600)  # Convert hours to seconds


# Global scheduler instance
scheduler = ScoreUpdateScheduler()


def start_scheduler():
    """Start the score update scheduler"""
    scheduler.start()


def stop_scheduler():
    """Stop the score update scheduler"""
    scheduler.stop()


def is_scheduler_running():
    """Check if the scheduler is currently running"""
    return scheduler.running
