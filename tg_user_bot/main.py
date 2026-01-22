from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from pyrogram.types import Message
import os, time, asyncio
from myapi import MyAPI


load_dotenv()
API_HASH = os.getenv("API_HASH")
API_ID = int(os.getenv("API_ID"))
PHONE_NUM = os.getenv("PHONE_NUM")
app = Client("user_bot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUM)
api = MyAPI()

@app.on_message((filters.group | filters.private | filters.channel) & (filters.text | filters.caption))
async def message_handler(client: Client, message: Message):
    chat = api.get_chat(message.chat.id)
    if not chat:
        return

    if chat.risk != 'risky':
        return
    
    text = (message.text or message.caption or "")
    result = api.check_message(text)
    if not result.get('ok'):
        print(result)
        return
    
    if result.get("ok"):
        label = result['result']['label']
        confidence = result['result']['confidence']
        if label in ['drug_ad', 'drug_related']:
            await message.reply_text(
                f"⚠️ This message was flagged as *{label}* with confidence *{confidence:.2f}*.\n\n"
                "Please review its content carefully."
            )
        
    
    


async def loop():
    while True:
        # api.get_chat
        await asyncio.sleep(5)



if __name__ == "__main__":
    asyncio.get_event_loop().create_task(loop())
    app.run()