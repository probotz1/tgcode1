import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.database.access_db import db
from utils.database.add_user import AddUserToDatabase
from utils.helper import check_chat, output, encode_video
from utils.settings import OpenSettings

# Bot configuration
from config import API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(level=logging.INFO)

app = Client("VideoEncoderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("reset"))
async def reset(bot: Client, update: Message):
    c = await check_chat(update, chat='Both')
    if not c:
        return
    await db.delete_user(update.from_user.id)
    await db.add_user(update.from_user.id)
    await update.reply(text="Settings reset successfully", reply_markup=output)

@app.on_message(filters.command("settings"))
async def settings_handler(bot: Client, event: Message):
    c = await check_chat(event, chat='Both')
    if not c:
        return
    await AddUserToDatabase(bot, event)
    editable = await event.reply_text("Please Wait ...")
    await OpenSettings(editable, user_id=event.from_user.id)

@app.on_message(filters.command("vset"))
async def settings_viewer(bot: Client, event: Message):
    c = await check_chat(event, chat='Both')
    if c is None:
        return
    await AddUserToDatabase(bot, event)
    # Rest of the code to fetch settings from the database and format the response

@app.on_message(filters.video)
async def video_handler(bot: Client, message: Message):
    video_file = await message.download()
    user_id = message.from_user.id
    settings = await db.get_user_settings(user_id)
    
    # Perform encoding
    output_file = await encode_video(video_file, settings)
    
    await message.reply_video(video=output_file)
    
    # Clean up
    os.remove(video_file)
    os.remove(output_file)

if __name__ == "__main__":
    app.run()

