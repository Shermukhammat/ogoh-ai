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
    text = (message.text or message.caption or "")
    print(f"{message.chat.type} {message.chat.id}: {text[:120]}")
    await message.reply_text("warning")


async def loop():
    while True:
        # api.get_chat
        await asyncio.sleep(5)



if __name__ == "__main__":
    asyncio.get_event_loop().create_task(loop())
    app.run()