import re

import requests
from WinxMusic import app
from config import LOG_GROUP_ID
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗨𝗥𝗟 𝗱𝗼 𝗿𝗲𝗲𝗹 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 📲"
        )
        return
    url = message.text.split()[1]
    if not re.match(
            re.compile(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$"), url
    ):
        return await message.reply_text(
            "𝗔 𝗨𝗥𝗟 𝗽𝗿𝗼𝘃𝗶𝗱𝗮 𝗻𝗮̃𝗼 𝗲́ 𝘃𝗮́𝗹𝗶𝗱𝗮 𝗽𝗮𝗿𝗮 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 😅"
        )
    a = await message.reply_text("𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...⏳")
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    response = requests.get(api_url)
    try:
        result = response.json()
        data = result["result"]
    except Exception as e:
        f = f"𝗘𝗿𝗿𝗼: \n{e} ❌"
        try:
            await a.edit(f)
        except Exception:
            await message.reply_text(f)
            return await app.send_message(LOG_GROUP_ID, f)
        return await app.send_message(LOG_GROUP_ID, f)
    if not result["error"]:
        video_url = data["url"]
        duration = data["duration"]
        quality = data["quality"]
        type = data["extension"]
        size = data["formattedSize"]
        caption = f"**𝗗𝘂𝗿𝗮𝗰̧𝗮̃𝗼:** {duration} 🕒\n**𝗤𝘂𝗮𝗹𝗶𝗱𝗮𝗱𝗲:** {quality} 📹\n**𝗧𝗶𝗽𝗼:** {type} 🎥\n**𝗧𝗮𝗺𝗮𝗻𝗵𝗼:** {size} 💾"
        await a.delete()
        await message.reply_video(video_url, caption=caption)
    else:
        try:
            return await a.edit("𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗯𝗮𝗶𝘅𝗮𝗿 𝗼 𝗿𝗲𝗲𝗹 ❗")
        except Exception:
            return await message.reply_text("𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗯𝗮𝗶𝘅𝗮𝗿 𝗼 𝗿𝗲𝗲𝗹 ❗")


__MODULE__ = "📲𝗥𝗲𝗲𝗹"
__HELP__ = """
**𝗕𝗮𝗶𝘅𝗮𝗱𝗼𝗿 𝗱𝗲 𝗿𝗲𝗲𝗹𝘀 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺:**

• `/ig [URL]`: 𝗕𝗮𝗶𝘅𝗮𝗿 𝗿𝗲𝗲𝗹𝘀 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺. 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗨𝗥𝗟 𝗱𝗼 𝗿𝗲𝗲𝗹 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼
• `/instagram [URL]`: 𝗕𝗮𝗶𝘅𝗮𝗿 𝗿𝗲𝗲𝗹𝘀 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺. 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗨𝗥𝗟 𝗱𝗼 𝗿𝗲𝗲𝗹 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼
• `/reel [URL]`: 𝗕𝗮𝗶𝘅𝗮𝗿 𝗿𝗲𝗲𝗹𝘀 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺. 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗨𝗥𝗟 𝗱𝗼 𝗿𝗲𝗲𝗹 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼
"""
