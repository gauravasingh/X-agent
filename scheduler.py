"""
Scheduler for running the agent on a daily basis
"""
import schedule
import time
from datetime import datetime
import subprocess
import sys


class AgentScheduler:
    def __init__(self, mode: str = "trending", run_time: str = "09:00"):
        """
        Initialize scheduler
        
        Args:
            mode: Agent mode (trending, keywords, full)
            run_time: Time to run in HH:MM format (24-hour)
        """
        self.mode = mode
        self.run_time = run_time
        self.schedule = schedule.Scheduler()
    
    def schedule_daily_run(self):
        """Schedule daily agent run"""
        self.schedule.every().day.at(self.run_time).do(self._run_agent)
        print(f"📅 Scheduled agent to run daily at {self.run_time}")
        print(f"   Mode: {self.mode}")
    
    def start(self):
        """Start the scheduler"""
        print("🕐 Scheduler started. Waiting for execution time...")
        print("   Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\n⏹️  Scheduler stopped by user")
    
    def _run_agent(self):
        """Execute the agent"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"⏰ Running scheduled agent: {timestamp}")
        print(f"{'='*60}\n")
        
        try:
            cmd = [sys.executable, "main.py", "--mode", self.mode, "--limit", "1000"]
            subprocess.run(cmd, check=True)
            print(f"\n✅ Agent run completed at {datetime.now().strftime('%H:%M:%S')}\n")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Agent run failed with error: {e}\n")


def run_scheduler():
    """Run the agent scheduler"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Schedule X Agent to run daily")
    parser.add_argument(
        "--time",
        default="09:00",
        help="Time to run agent daily (HH:MM format, default: 09:00)"
    )
    parser.add_argument(
        "--mode",
        choices=["trending", "keywords", "full"],
        default="trending",
        help="Agent mode"
    )
    
    args = parser.parse_args()
    scheduler = AgentScheduler(mode=args.mode, run_time=args.time)
    scheduler.schedule_daily_run()
    scheduler.start()


if __name__ == "__main__":
    run_scheduler()
