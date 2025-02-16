import random

import requests
from Cecilia import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@app.on_message(filters.command(["wall", "wallpaper"]))
async def wall(_, message: Message):
    try:
        text = message.text.split(None, 1)[1]
    except IndexError:
        text = None
    if not text:
        return await message.reply_text(
            "⚠️ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘂𝗺𝗮 𝗽𝗮𝗹𝗮𝘃𝗿𝗮 𝗽𝗮𝗿𝗮 𝗽𝗲𝘀𝗾𝘂𝗶𝘀𝗮𝗿.")
    m = await message.reply_text("🔍 𝗣𝗲𝘀𝗾𝘂𝗶𝘀𝗮𝗻𝗱𝗼...")
    try:
        url = requests.get(f"https://api.safone.dev/wall?query={text}").json()[
            "results"
        ]
        ran = random.randint(0, 7)
        await message.reply_photo(
            photo=url[ran]["imageUrl"],
            caption=f"🥀 **𝗦𝗼𝗹𝗶𝗰𝗶𝘁𝗮𝗱𝗼 𝗽𝗼𝗿 :** {message.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🌐 𝗟𝗶𝗻𝗸", url=url[ran]["imageUrl"])],
                ]
            ),
        )
        await m.delete()
    except Exception as e:
        await m.edit_text(
            f"⚠️ 𝗡𝗲𝗻𝗵𝘂𝗺 𝗽𝗮𝗽𝗲𝗹 𝗱𝗲 𝗽𝗮𝗿𝗲𝗱𝗲 𝗳𝗼𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 : `{text}`",
        )


__MODULE__ = "🖼️𝗪𝗮𝗹𝗹"
__HELP__ = """
📌 **𝗖𝗢𝗠𝗔𝗡𝗗𝗢𝗦:**

• /𝗪𝗔𝗟𝗟 - **𝗗𝗲𝘀𝗰𝗮𝗿𝗴𝗮𝗿 𝗲 𝗲𝗻𝘃𝗶𝗮𝗿 𝘂𝗺 𝗽𝗮𝗽𝗲𝗹 𝗱𝗲 𝗽𝗮𝗿𝗲𝗱𝗲.**

📖 **𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗖̧𝗢̃𝗘𝗦:**

- 𝗘𝘀𝘁𝗲 𝗯𝗼𝘁 𝗽𝗿𝗲𝗻𝘀𝗲𝗻𝘁𝗮 𝘂𝗺 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝗱𝗲𝘀𝗰𝗮𝗿𝗴𝗮 𝗲 𝗲𝗻𝘃𝗶𝗼 𝗱𝗲 𝗽𝗮𝗽𝗲𝗶𝘀 𝗱𝗲 𝗽𝗮𝗿𝗲𝗱𝗲.
- 𝗨𝘁𝗶𝗹𝗶𝘇𝗲 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /𝗪𝗔𝗟𝗟 𝗰𝗼𝗺 𝘂𝗺𝗮 𝗽𝗮𝗹𝗮𝘃𝗿𝗮 𝗽𝗮𝗿𝗮 𝗽𝗲𝘀𝗾𝘂𝗶𝘀𝗮𝗿 𝗲𝗻𝘃𝗶𝗮𝗿 𝗽𝗮𝗽𝗲𝗹 𝗱𝗲 𝗽𝗮𝗿𝗲𝗱𝗲 𝗻𝗼 𝗰𝗵𝗮𝘁.

📢 **𝗡𝗢𝗧𝗔:**

- 𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗼𝗱𝗲 𝘀𝗲𝗿 𝘂𝘁𝗶𝗹𝗶𝘇𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 𝗱𝗲𝘀𝗰𝗮𝗿𝗴𝗮𝗿 𝗲 𝗲𝗻𝘃𝗶𝗮𝗿 𝗽𝗮𝗽𝗲𝗹 𝗱𝗲 𝗽𝗮𝗿𝗲𝗱𝗲.
"""
