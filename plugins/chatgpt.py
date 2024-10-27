from TheApi import api
from WinxMusic import app
from config import BANNED_USERS
from pyrogram import filters, Client
from pyrogram.enums import ChatAction
from pyrogram.types import Message


@app.on_message(filters.command(["chatgpt", "ai", "ask"]) & ~BANNED_USERS)
async def chatgpt_chat(bot: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "💡 **Exemplo de uso:**\n\n`/ai escreva um código simples de site usando HTML, CSS e JS?`"
        )
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    results = api.chatgpt(user_input)
    await message.reply_text(f"🤖 **Resposta:**\n\n{results}")


__MODULE__ = "🤖 𝗖𝗵𝗮𝘁𝗚𝗣𝗧"
__HELP__ = """
**𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀:**

• /advice - **𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝘂𝗺 𝗰𝗼𝗻𝘀𝗲𝗹𝗵𝗼 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗼 𝗱𝗼 𝗯𝗼𝘁**
• /ai [𝘀𝘂𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮] - **𝗙𝗮𝘇𝗮 𝘂𝗺𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮 𝗮 𝗔𝗜 𝗱𝗼 𝗖𝗵𝗮𝘁𝗚𝗣𝗧**
• /gemini [𝘀𝘂𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮] - **𝗙𝗮𝘇𝗮 𝘂𝗺𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮 𝗮 𝗔𝗜 𝗚𝗲𝗺𝗶𝗻𝗶 𝗱𝗮 𝗚𝗼𝗼𝗴𝗹𝗲**
• /bard [𝘀𝘂𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮] - **𝗙𝗮𝘇𝗮 𝘂𝗺𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮 𝗮 𝗕𝗮𝗿𝗱 𝗔𝗜 𝗱𝗮 𝗚𝗼𝗼𝗴𝗹𝗲**
"""
