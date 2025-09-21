import time
import yaml
import croniter
import logging
from datetime import datetime
from lib.broadcaster import Broadcaster

# Configure logging
logging.basicConfig(
    filename='run.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('croner.py')

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
        logger.info("Starting scheduler...")
        
        while True:
            try:
                config = self.load_config()
                logger.info(f"Loaded configuration with {len(config.get('broadcasts', []))} broadcasts")
                
                for broadcast in config.get('broadcasts', []):
                    broadcast_id = broadcast.get('id')
                    logger.info(f"Processing broadcast: {broadcast_id}")
                    
                    cron_data = self.get_or_create_cron(broadcast)
                    should_run = self.broadcaster.process(broadcast, cron_data)
                    
                    if should_run:
                        logger.info(f"Broadcast {broadcast_id} was sent")
                    else:
                        logger.info(f"Broadcast {broadcast_id} was skipped (not scheduled to run)")
                    cron_data['last_run'] = datetime.now()
                
                # Sleep for a minute before checking again
                time.sleep(60)
                
            except Exception as e:
                error_msg = f"Error in scheduler loop: {e}"
                print(error_msg)
                logger.error(error_msg)
                time.sleep(60)  # Sleep and try again