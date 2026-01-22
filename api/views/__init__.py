from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
import os 


load_dotenv()
REST_API_TOKEN = os.getenv("REST_API_TOKEN")

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        token = request.query_params.get('token') or request.data.get('token')
        if token != REST_API_TOKEN:
            raise AuthenticationFailed('Invalid token')
        return (None, None)  

from .ads_model import classify_ads_api, check_message
from .tg_chats import TelegramChatViewSet, get_new_chat, get_chat