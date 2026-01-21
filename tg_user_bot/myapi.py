import requests
from datetime import datetime, timezone, timedelta


class ChatType:
    CHANNEL = "channel"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    USER = "user"

class TgChat:
    def __init__(self, tg_id : int = None,
                 chat_type : str = None,
                 title : str = None,
                 first_name : str = None,
                 last_name : str = None,
                 username : str = None,
                 description : str = None,
                 members_count : int = None,
                 last_checked_message_id : int = None,
                 is_safe : bool = None,
                 risk_score : float = None,
                 discovered_by : str = None,
                 created_at : str = None,
                 last_checked_at : str = None):
        self.tg_id = tg_id
        self.chat_type = chat_type
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.description = description
        self.members_count = members_count
        self.last_checked_message_id = last_checked_message_id
        self.is_safe = is_safe
        self.risk_score = risk_score
        self.discovered_by = discovered_by
        self.created_at = created_at
        self.last_checked_at = last_checked_at

    


class MyAPI:
    def __init__(self, base_url: str = '127.0.0.1:8000', token: str = 'blah'):
        self.BASE_URL = base_url
        self.TOKEN = token 

    def get_chat(self, tg_id: int) -> TgChat:
        url = f"http://{self.BASE_URL}/api/tg_chats/{tg_id}/?token={self.TOKEN}"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        chat = TgChat(
            tg_id=data.get('tg_id'),
            chat_type=data.get('type'),
            title=data.get('title'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            created_at=data.get('created_at'),
            last_checked_at=data.get('last_checked_at')
        )
        return chat
    
