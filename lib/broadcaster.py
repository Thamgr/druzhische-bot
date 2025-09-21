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
        now = datetime.now()
        cron = cron_data['cron']
        last_run = cron_data['last_run']
        
        next_time = cron.get_next(datetime, start_time=last_run)
        return now >= next_time
    
    def get_module(self, module_name):
        try:
            module_path = f"lib.modules.{module_name.lower()}"
            module = importlib.import_module(module_path)
            return getattr(module, module_name)()
        except (ImportError, AttributeError) as e:
            print(f"Error loading module {module_name}: {e}")
            return None
    
    def process(self, broadcast, cron_data):
        if self.should_broadcast(broadcast, cron_data):
            module_name = broadcast.get('module')
            module = self.get_module(module_name)
            
            if module:
                message = module.render(broadcast)
                chat_id = broadcast.get('chat_id')
                
                if message and chat_id:
                    print(f"Broadcasting message {broadcast['id']} to chat {chat_id}")
                    logger.info(f"Broadcasting message {broadcast['id']} to chat {chat_id}")
                    logger.info(f"Message content: {message[:100]}{'...' if len(message) > 100 else ''}")
                    self.sender.send(chat_id, message)
                    return True
        
        return False
