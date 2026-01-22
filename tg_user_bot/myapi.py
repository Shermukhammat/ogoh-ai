import requests
from datetime import datetime, timezone, timedelta


class ChatType:
    CHANNEL = "channel"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    USER = "user"

class TgChat:
    def __init__(self, data: dict):
        self.id = data.get('id')
        self.tg_id = data.get('tg_id')
        self.username = data.get('username')
        self.chat_type = data.get('type')
        self.title = data.get('title')
        self.description = data.get('description')
        self.risk = data.get('risk')
        
        self.invate_link = data.get('invate_link')
        self.created_at = data.get('created_at')


    


class MyAPI:
    def __init__(self, base_url: str = '127.0.0.1:8000', token: str = 'blah'):
        self.BASE_URL = base_url
        self.TOKEN = token 

    def get_chat(self, tg_id: int) -> TgChat:
        url = f"http://{self.BASE_URL}/api/tg_chat"
        response = requests.get(url, params={'token': self.TOKEN, 'tg_id': tg_id})
        if response.status_code != 200:
            return None
        data = response.json()
        return TgChat(data)
    
    def get_new_chat(self) -> list[TgChat]:
        url = f"http://{self.BASE_URL}/api/get_new_chat/?token={self.TOKEN}"
        response = requests.get(url)
        if response.status_code != 200:
            return []
        data = response.json()
        if not data.get('ok'):
            return []
        chat_data = data.get('chats')
        return [TgChat(chat) for chat in chat_data]
    
    def check_message(self, message: str) -> dict:
        url = f"http://{self.BASE_URL}/api/check_message"
        response = requests.get(url, params={'token': self.TOKEN, 'message': message})
        if response.status_code != 200:
            return {"ok": False, "error": "Request failed"}
        data = response.json()
        return data

    def create_warning_message(self, chat_id: int, message_id: int, content: str, user_id: int = None) -> dict:
        url = f"http://{self.BASE_URL}/api/create_warning"
        json_data = {"token": self.TOKEN,
                     "chat_id": chat_id,
                     "message_id": message_id,
                      "content": content}
        resp = requests.post(url, json=json_data)
        print(resp.json())
        if resp.status_code != 200:
            return True
        return False

    
