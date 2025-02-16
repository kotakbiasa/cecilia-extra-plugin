import asyncio
from random import choice

import pyfiglet
from Cecilia import app
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


def figle(text):
    x = pyfiglet.FigletFont.getFonts()
    font = choice(x)
    figled = str(pyfiglet.figlet_format(text, font=font))
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🔄 **𝗧𝗿𝗼𝗰𝗮𝗿**", callback_data="figlet"),
                InlineKeyboardButton(text="❌ **𝗙𝗲𝗰𝗵𝗮𝗿**", callback_data="close_reply"),
            ]
        ]
    )
    return figled, keyboard


@app.on_message(filters.command("figlet"))
async def echo(bot, message):
    global text
    try:
        text = message.text.split(" ", 1)[1]
    except IndexError:
        return await message.reply_text("💡 **𝗘𝘅𝗲𝗺𝗽𝗹𝗼 𝗱𝗲 𝘂𝘀𝗼:**\n\n`/figlet OpenAI`")
    kul_text, keyboard = figle(text)
    await message.reply_text(
        f"🎨 **𝗔𝗾𝘂𝗶 𝗲𝘀𝘁𝗮́ 𝘀𝗲𝘂 𝗙𝗶𝗴𝗹𝗲𝘁:**\n<pre>{kul_text}</pre>",
        quote=True,
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("figlet"))
async def figlet_handler(Client, query: CallbackQuery):
    try:
        kul_text, keyboard = figle(text)
        await query.message.edit_text(
            f"🎨 **𝗔𝗾𝘂𝗶 𝗲𝘀𝘁𝗮́ 𝘀𝗲𝘂 𝗙𝗶𝗴𝗹𝗲𝘁:**\n<pre>{kul_text}</pre>", reply_markup=keyboard
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)

    except Exception as e:
        return await query.answer(e, show_alert=True)


__MODULE__ = "🎨 𝗙𝗶𝗴𝗹𝗲𝘁"
__HELP__ = """
**𝗙𝗶𝗴𝗹𝗲𝘁**

• /figlet <texto> - **𝗖𝗿𝗶𝗮 𝘂𝗺 𝗙𝗶𝗴𝗹𝗲𝘁 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗼 𝘁𝗲𝘅𝘁𝗼 𝗳𝗼𝗿𝗻𝗲𝗰𝗶𝗱𝗼.**
"""
