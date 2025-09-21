import time
import yaml
import croniter
from datetime import datetime
from lib.broadcaster import Broadcaster

class Scheduler:
    def __init__(self, config_path='config.yml'):
        self.config_path = config_path
        self.broadcaster = Broadcaster()
        self.crons = {}  # Map to store croniter instances for each broadcast
    
    def load_config(self):
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def get_or_create_cron(self, broadcast):
        broadcast_id = broadcast['id']
        schedule = broadcast['schedule']
        
        if broadcast_id not in self.crons:
            now = datetime.now()
            cron = croniter.croniter(schedule, now)
            self.crons[broadcast_id] = {
                'cron': cron,
                'last_run': None
            }
        
        return self.crons[broadcast_id]
    
    def run(self):
        print("Starting scheduler...")
        
        while True:
            try:
                config = self.load_config()
                
                for broadcast in config.get('broadcasts', []):
                    cron_data = self.get_or_create_cron(broadcast)
                    should_run = self.broadcaster.process(broadcast, cron_data)
                    
                    if should_run:
                        cron_data['last_run'] = datetime.now()
                
                # Sleep for a minute before checking again
                time.sleep(60)
                
            except Exception as e:
                print(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Sleep and try again