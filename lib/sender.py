import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get logger
logger = logging.getLogger('sender.py')

class Sender:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sender, cls).__new__(cls)
            # Get token from environment variable
            cls._instance.token = os.getenv("BOT_TOKEN")
        return cls._instance
    
    def send(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        try:
            response = requests.post(url, data=data)
            result = response.json()
            logger.info(f"Message sent to chat {chat_id}, response: {result}")
            return result
        except Exception as e:
            error_msg = f"Error sending message: {e}"
            print(error_msg)
            logger.error(error_msg)
            return None