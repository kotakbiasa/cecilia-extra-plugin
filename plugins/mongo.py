import re

from WinxMusic import app
from pymongo import MongoClient
from pyrogram import filters, Client
from pyrogram.types import Message

mongo_url_pattern = re.compile(r"mongodb(?:\+srv)?:\/\/[^\s]+")


@app.on_message(filters.command("mongochk"))
async def mongo_command(_client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply(
            "𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗶𝗻𝘀𝗶𝗿𝗮 𝘀𝗲𝘂 𝗹𝗶𝗻𝗸 𝗠𝗼𝗻𝗴𝗼𝗗𝗕 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 `/mongochk seu_mongodb_url` 📥"
        )
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            client.server_info()
            await message.reply(
                "✅ 𝗨𝗿𝗹 𝗱𝗼 𝗠𝗼𝗻𝗴𝗼𝗗𝗕 𝗲́ 𝘃𝗮́𝗹𝗶𝗱𝗮 𝗲 𝗮 𝗰𝗼𝗻𝗲𝘅𝗮̃𝗼 𝗳𝗼𝗶 𝘀𝘂𝗰𝗲𝘀𝘀𝗼𝘀𝗮!")
        except Exception as e:
            await message.reply(f"⚠️ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗰𝗼𝗻𝗲𝗰𝘁𝗮𝗿 𝗼 𝗠𝗼𝗻𝗴𝗼𝗗𝗕: {e}")
    else:
        await message.reply("🚫 𝗢𝗼𝗽𝘀! 𝗢 𝗳𝗼𝗿𝗺𝗮𝘁𝗼 𝗱𝗼 𝘀𝗲𝘂 𝗹𝗶𝗻𝗸 𝗠𝗼𝗻𝗴𝗼𝗗𝗕 𝗲́ 𝗶𝗻𝘃𝗮́𝗹𝗶𝗱𝗼.")


__MODULE__ = "🛢️𝗠𝗼𝗻𝗴𝗼𝗗𝗕"
__HELP__ = """
**𝗖𝗵𝗲𝗰𝗮𝗴𝗲𝗺 𝗱𝗲 𝗠𝗼𝗻𝗴𝗼𝗗𝗕:**

• `/mongochk [mongo_url]`: 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮 𝗮 𝘃𝗮́𝗹𝗶𝗱𝗮𝗱𝗲 𝗲 𝗰𝗼𝗻𝗲𝘅𝗮̃𝗼 𝗱𝗲 𝘂𝗺 𝗹𝗶𝗻𝗸 𝗱𝗼 𝗠𝗼𝗻𝗴𝗼𝗗𝗕 𝗮 𝘂𝗺𝗮 𝗶𝗻𝘀𝘁𝗮𝗻𝗰𝗶𝗮.
"""
