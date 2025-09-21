import importlib
from datetime import datetime
from lib.sender import Sender

class Broadcaster:
    def __init__(self):
        self.sender = Sender()
    
    def should_broadcast(self, broadcast, cron_data):
        now = datetime.now()
        cron = cron_data['cron']
        last_run = cron_data['last_run']
        
        # If we've never sent this broadcast before
        if last_run is None:
            next_time = cron.get_prev(datetime)
            # Check if the next time is within the last hour (to avoid immediate sending on startup)
            return (now - next_time).total_seconds() < 3600
        
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
                    self.sender.send(chat_id, message)
                    return True
        
        return False
