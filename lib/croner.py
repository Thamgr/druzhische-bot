import time
import logging
from lib.broadcaster import Broadcaster
from lib.configer import Configer

# Configure logging
logging.basicConfig(
    filename='run.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('croner.py')

class Scheduler:
    def __init__(self):
        self.broadcaster = Broadcaster()
    
    def run(self):
        print("Starting scheduler...")
        logger.info("Starting scheduler...")
        
        while True:
            try:
                configs = Configer.Get()
                logger.info(f"Loaded configuration with {len(configs)} broadcasts")
                
                for config in configs:
                    logger.info(f"Processing broadcast: {config.id}")
                    self.broadcaster.process(config)
                
                # Sleep for a minute before checking again
                time.sleep(30)
                
            except Exception as e:
                error_msg = f"Error in scheduler loop: {e}"
                logger.error(error_msg)
                time.sleep(30)  # Sleep and try again