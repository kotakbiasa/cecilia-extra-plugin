import requests
from MukeshAPI import api
from WinxMusic import app
from pyrogram import filters, Client
from pyrogram.enums import ChatAction
from pyrogram.types import Message


@app.on_message(filters.command(["gemini"]))
async def gemini_handler(_client: Client, message: Message):
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)
    if (
            message.text.startswith(f"/gemini@{app.username}")
            and len(message.text.split(" ", 1)) > 1
    ):
        user_input = message.text.split(" ", 1)[1]
    elif message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        if len(message.command) > 1:
            user_input = " ".join(message.command[1:])
        else:
            await message.reply_text("𝗘𝘅𝗲𝗺𝗽𝗹𝗼 :- `/gemini quem é o senhor ram`")
            return

    try:
        response = api.gemini(user_input)
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        x = response["results"]
        if x:
            await message.reply_text(x, quote=True)
        else:
            await message.reply_text("𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲! 𝗧𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲.")
    except requests.exceptions.RequestException as e:
        await message.reply_text("𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗿 𝗮 𝗿𝗲𝗾𝘂𝗶𝘀𝗶𝗰̧𝗮̃𝗼.")
