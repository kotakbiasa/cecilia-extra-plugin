import requests
from SafoneAPI import SafoneAPI
from Cecilia import app
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command(["bard"]))
async def bard(bot, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "💡 **𝗘𝘅𝗲𝗺𝗽𝗹𝗼 𝗱𝗲 𝘂𝘀𝗼:**\n\n`/bard conte-me brevemente sobre Rama e Sita.`"
        )
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])

    try:
        Z = await SafoneAPI().bard(user_input)
        result = Z["candidates"][0]["content"]["parts"][0]["text"]
        await message.reply_text(f"📖 **𝗥𝗲𝘀𝘂𝗹𝘁𝗮𝗱𝗼:**\n\n{result}")
    except requests.exceptions.RequestException as e:
        await message.reply_text(
            "⚠️ **𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼 𝗮𝗼 𝘁𝗲𝗻𝘁𝗮𝗿 𝗯𝘂𝘀𝗰𝗮𝗿 𝗮 𝗿𝗲𝘀𝗽𝗼𝘀𝘁𝗮. 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲.**")
