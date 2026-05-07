from pyrogram import Client, filters
from PIL import Image
import os

API_ID = 36634326
API_HASH = "e22f4c699919368d6d1f66ee2118a658"
BOT_TOKEN = "8798591404:AAFnXxlmRwWyCkU8o89MfD4NPIT7imKtdAM"

CHANNEL = "@E26RRN"

app = Client(
    "thumb-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user_data = {}

@app.on_message(filters.private & filters.document)
async def get_file(client, message):
    path = await message.download()
    user_data[message.chat.id] = {"file": path}
    await message.reply("Thumbnail image එක send කරන්න.")

@app.on_message(filters.private & filters.photo)
async def get_thumb(client, message):
    path = await message.download()

    img = Image.open(path)
    img.thumbnail((320, 320))
    thumb_path = "thumb.jpg"
    img.save(thumb_path)

    user_data[message.chat.id]["thumb"] = thumb_path

    await message.reply("Caption එක send කරන්න.")

@app.on_message(filters.private & filters.text)
async def upload_file(client, message):
    if message.chat.id not in user_data:
        return

    caption = message.text

    file_path = user_data[message.chat.id]["file"]
    thumb_path = user_data[message.chat.id]["thumb"]

    await client.send_document(
        chat_id=CHANNEL,
        document=file_path,
        thumb=thumb_path,
        caption=caption
    )

    await message.reply("Upload complete ✅")

app.run()
