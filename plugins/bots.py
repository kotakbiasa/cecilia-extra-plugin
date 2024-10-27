import asyncio

from WinxMusic import app
from pyrogram import enums, filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message


@app.on_message(filters.command("bots") & filters.group)
async def bots(_client: Client, message: Message):
    try:
        bot_list = []
        async for bot in app.get_chat_members(
                message.chat.id, filter=enums.ChatMembersFilter.BOTS
        ):
            bot_list.append(bot.user)
        len_bot_list = len(bot_list)
        text3 = f"**🤖 𝗟𝗶𝘀𝘁𝗮 𝗱𝗲 𝗕𝗼𝘁𝘀 - {message.chat.title}**\n\n𝗕𝗼𝘁𝘀:\n"
        while len(bot_list) > 1:
            bot = bot_list.pop(0)
            text3 += f"├ @{bot.username}\n"
        else:
            bot = bot_list.pop(0)
            text3 += f"└ @{bot.username}\n\n"
            text3 += f"**𝗧𝗼𝘁𝗮𝗹 𝗱𝗲 𝗯𝗼𝘁𝘀:** {len_bot_list}"
            await app.send_message(message.chat.id, text3)
    except FloodWait as e:
        await asyncio.sleep(e.value)


__MODULE__ = "🤖 𝗕𝗼𝘁𝘀"
__HELP__ = """
**𝗕𝗼𝘁𝘀**

• /bots - **𝗢𝗯𝘁𝗲́𝗺 𝘂𝗺𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝗯𝗼𝘁𝘀 𝗻𝗼 𝗴𝗿𝘂𝗽𝗼.**
"""
