from dotenv import load_dotenv
from pyrogram import Client 
from pyrogram.types import Message
import os


load_dotenv()
API_HASH=os.getenv("API_HASH")
API_ID=int(os.getenv("API_ID"))
PHONE_NUM=os.getenv("PHONE_NUM")

clent = Client("user_bot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUM)

with clent:
    # clent.send_message("@TemirovDS", "Salom botd")
    # query = "tez yetkazish"
    # for d in clent.get_dialogs():
    #     if d.chat.title:
    #         print(d.chat.title)
    results = clent.get_chat_history(chat_id=-1002598868618, limit=10)

    for message in results:
        if not isinstance(message, Message):
            continue
        if message.text:
            print(message.text)
        elif message.photo or message.document or message.video and message.caption:
            print("Media message caption:", message.caption)