import importlib
import logging
from datetime import datetime
from lib.sender import Sender

# Get logger
logger = logging.getLogger('broadcaster.py')

class Broadcaster:
    def __init__(self):
        self.sender = Sender()
    
    def should_broadcast(self, broadcast, cron_data):
        broadcast_id = broadcast.get('id')
        logger.info(f"Checking if broadcast {broadcast_id} should run")
        
        now = datetime.now()
        cron = cron_data['cron']
        last_run = cron_data['last_run']
        
        next_time = cron.get_next(datetime, start_time=last_run)
        should_run = now >= next_time
        logger.info(f"Broadcast {broadcast_id} should run: {should_run}, next_time: {next_time}, last_run: {last_run}")
        return should_run
    
    def get_module(self, module_name):
        module_path = f"lib.modules.{module_name}"
        logger.info(f"Module path: {module_path}")
        module = importlib.import_module(module_path)
        instance = getattr(module, module_name)()
        return instance
    
    def process(self, broadcast, cron_data):
        if not self.should_broadcast(broadcast, cron_data):
            return
        module_name = broadcast.get('module')
        module = self.get_module(module_name)

        message = module.render(broadcast)
        chat_id = broadcast.get('chat_id')
        logger.info(f"Broadcasting message {broadcast['id']} to chat {chat_id}")
        self.sender.send(chat_id, message)
