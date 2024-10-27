from WinxMusic import app
from WinxMusic.utils.functions import MARKDOWN
from pyrogram.enums import ChatType, ParseMode
from pyrogram.filters import command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@app.on_message(command("markdownhelp"))
async def mkdwnhelp(_, m: Message):
    keyb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="👉 𝗖𝗹𝗶𝗾𝘂𝗲 𝗮𝗾𝘂𝗶!",
                    url=f"http://t.me/{app.username}?start=mkdwn_help",
                )
            ]
        ]
    )
    if m.chat.type != ChatType.PRIVATE:
        await m.reply(
            "📥 𝗖𝗹𝗶𝗾𝘂𝗲 𝗻𝗼 𝗯𝗼𝘁𝗮̃𝗼 𝗮𝗯𝗮𝗶𝘅𝗼 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗮 𝘀𝗶𝗻𝘁𝗮𝘅𝗲 𝗱𝗲 𝘂𝘀𝗼 𝗱𝗼 𝗺𝗮𝗿𝗸𝗱𝗼𝘄𝗻 𝗻𝗼 𝗽𝗿𝗶𝘃𝗮𝗱𝗼!",
            reply_markup=keyb,
        )
    else:
        await m.reply(
            MARKDOWN, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
    return
