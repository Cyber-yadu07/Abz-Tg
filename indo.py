from pyrogram import Client, filters, idle
from pyrogram.types import ChatJoinRequest
import os
import asyncio
import logging
from pyrogram.errors import FloodWait, MessageNotModified
import dotenv
import time

start_time = time.time()


dotenv.load_dotenv()

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    datefmt="[%d/%m/%Y %H:%M:%S]",
    format=" %(asctime)s - [INDOAPPROVEBOT] >> %(levelname)s << %(message)s",
    handlers=[logging.FileHandler("indoapprovebot.log"), logging.StreamHandler()])

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
chat_id = int(os.environ.get("CHAT_ID"))
owner_id = int(os.environ.get("OWNER_ID"))


bot_client = Client("INDOAPPROVEBOT", bot_token=bot_token, api_id=api_id, api_hash=api_hash)

@bot_client.on_chat_join_request(filters.chat(chat_id))
async def approve(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        logging.info(f"Sleeping for {e.x + 2} seconds due to floodwaits!")
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
 

@bot_client.on_message(filters.user(owner_id) & filters.command("alive", "!"))
async def well_yes(c, m):
    uptime_ = round(time.time() - start_time, 2)
    await m.reply_text(f"Yo bici its {c.my_bot.username}, i am alive! \n**UPTIME :** {uptime_}")
    
@bot_client.on_message(filters.command("start", ["/", "!"]))
async def hmm(c, m):
    await m.reply_animation("funny-where-do-you-come-from.mp4", quote=True)

async def run_bot_():
    logging.info("-----------------------------------------------")
    await bot_client.start()
    bot_client.my_bot = await bot_client.get_me()
    logging.info(f"Started bot as : {bot_client.my_bot.username}")
    end_time = round(time.time() - start_time, 2)
    logging.info(f"Deployed in {end_time}s")
    logging.info("-----------------------------------------------")
    await idle()

if __name__ == "__main__":
    bot_client.loop.run_until_complete(run_bot_())
