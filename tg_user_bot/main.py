from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from pyrogram.types import Message
import os, time, asyncio
from myapi import MyAPI
from asyncio import Semaphore
from pyrogram.enums import ChatType


load_dotenv()
API_HASH = os.getenv("API_HASH")
API_ID = int(os.getenv("API_ID"))
PHONE_NUM = os.getenv("PHONE_NUM")
app = Client("user_bot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUM)
api = MyAPI()
sema = Semaphore()

@app.on_message((filters.group | filters.private | filters.channel) & (filters.text | filters.caption))
async def message_handler(client: Client, message: Message):
    chat = api.get_chat(message.chat.id)
    if not chat:
        return

    if chat.risk != 'risky':
        return
    
    text = (message.text or message.caption or "")
    async with sema:
        result = api.check_message(text)

    print("result:", result)
    if not result.get('ok'):
        print('check message:', result)
        return
    
    if result.get("ok"):
        label = result['result']['label']
        confidence = result['result']['confidence']
        if label in ['drug_ad', 'drug_related']:
            print(message.chat.type)
            if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                await message.reply_text(
                f"⚠️ Ushbu xabar *{label}*  deb belgilandi *{confidence:.2f}* aniqlik bilan.\n\n")

            api.create_warning_message(message.chat.id, message.id, text, user_id=message.from_user.id if message.from_user else None)
        
    
    


async def loop():
    while True:
        # api.get_chat
        await asyncio.sleep(5)



if __name__ == "__main__":
    asyncio.get_event_loop().create_task(loop())
    app.run()