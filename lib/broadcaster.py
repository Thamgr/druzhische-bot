import logging
from datetime import datetime
from lib.sender import Sender
from lib.global_data import GlobalData

# Get logger
logger = logging.getLogger('broadcaster.py')

class Broadcaster:
    def __init__(self):
        self.sender = Sender()
    
    def should_broadcast(self, config):
        last_run = GlobalData().get_last_run(config.id)
        now = datetime.now()
        
        # Get next run time based on schedule and last run
        next_time = config.schedule.get_next(datetime, start_time=last_run)
        should_run = now >= next_time
        
        logger.info(f"Broadcast {config.id} should run: {should_run}, next_time: {next_time}, last_run: {last_run}")
        return should_run
    
    def process(self, config):
        """Process a broadcast config and return True if broadcast was sent"""
        if not self.should_broadcast(config):
            return False
        
        # Render message using the module - pass just the text for minimalism
        message = config.module.render(config.text)
        
        # Send the message
        logger.info(f"Broadcasting message {config.id} to chat {config.chat_id}")
        self.sender.send(config.chat_id, message)
        GlobalData().update_last_run(config.id)

