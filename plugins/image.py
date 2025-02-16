from TheApi import api
from Cecilia import app
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import InputMediaPhoto, Message


@app.on_message(filters.command(["image"], prefixes=["/", "!", "."]) & ~BANNED_USERS)
async def image_from_bing(_, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("𝗜𝗻𝘀𝗶𝗿𝗮 𝗼 𝗻𝗼𝗺𝗲 𝗱𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗯𝘂𝘀𝗰𝗮𝗿 🔍")

    if message.reply_to_message and message.reply_to_message.text:
        query = message.reply_to_message.text
    else:
        query = " ".join(message.command[1:])

    messagesend = await message.reply_text("🔍 𝗕𝘂𝘀𝗰𝗮𝗻𝗱𝗼 𝗶𝗺𝗮𝗴𝗲𝗻𝘀...")

    media_group = []
    for url in api.bing_image(query, 6):
        media_group.append(InputMediaPhoto(media=url))
    await messagesend.edit("𝗖𝗮𝗿𝗿𝗲𝗴𝗮𝗻𝗱𝗼... 📤")
    try:
        await app.send_media_group(message.chat.id, media_group)
        await messagesend.delete()
    except Exception as e:
        await messagesend.edit(f"𝗘𝗿𝗿𝗼: {e} ❗")
