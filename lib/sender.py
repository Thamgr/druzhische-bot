import requests

class Sender:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sender, cls).__new__(cls)
            cls._instance.token = "YOUR_BOT_TOKEN"  # Replace with actual token
        return cls._instance
    
    def send(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return None