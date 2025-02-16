from SafoneAPI import SafoneAPI
from TheApi import api
from Cecilia import app
from config import LOG_GROUP_ID
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command("advice"))
async def advice(_, message: Message):
    A = await message.reply_text("...")
    res = api.get_advice()
    await A.edit(res)


@app.on_message(filters.command("astronomical"))
async def advice(_, message: Message):
    a = await SafoneAPI().astronomy()
    if a["success"]:
        c = a["date"]
        url = a["imageUrl"]
        b = a["explanation"]
        caption = f"🌌 **𝗘𝘃𝗲𝗻𝘁𝗼 𝗮𝘀𝘁𝗿𝗼𝗻𝗼̂𝗺𝗶𝗰𝗼 𝗱𝗲 𝗵𝗼𝗷𝗲 [{c}]:**\n\n{b}"
        await message.reply_photo(url, caption=caption)
    else:
        await message.reply_photo("🚫 **𝗧𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗱𝗮𝗾𝘂𝗶 𝗮 𝗽𝗼𝘂𝗰𝗼!**")
        await app.send_message(LOG_GROUP_ID, "⚠️ **/astronomical 𝗻𝗮̃𝗼 𝗲𝘀𝘁𝗮́ 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮𝗻𝗱𝗼.**")


__MODULE__ = "📝 𝗖𝗼𝗻𝘀𝗲𝗹𝗵𝗼"
__HELP__ = """
/advice - 💡 **𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝘂𝗺 𝗰𝗼𝗻𝘀𝗲𝗹𝗵𝗼 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗼**
/astronomical - 🌌 **𝗣𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗼 𝗳𝗮𝘁𝗼 𝗮𝘀𝘁𝗿𝗼𝗻𝗼̂𝗺𝗶𝗰𝗼 𝗱𝗲 𝗵𝗼𝗷𝗲**
"""
