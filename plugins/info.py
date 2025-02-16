import os

from Cecilia import app
from Cecilia.misc import SUDOERS
from Cecilia.utils.database import is_gbanned_user
from pyrogram import enums, filters
from pyrogram.types import Message

n = "\n"
w = " "


def bold(x):
    return f"**{x}:** "


def bold_ul(x):
    return f"**--{x}:**-- "


def mono(x):
    return f"`{x}`{n}"


def section(
        title: str,
        body: dict,
        indent: int = 2,
        underline: bool = False,
) -> str:
    text = (bold_ul(title) + n) if underline else bold(title) + n

    for key, value in body.items():
        if value is not None:
            text += (
                    indent * w
                    + bold(key)
                    + (
                        (value[0] + n)
                        if isinstance(value, list) and isinstance(value[0], str)
                        else mono(value)
                    )
            )
    return text


async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        x = user.status
        if x == enums.UserStatus.RECENTLY:
            return "🟢 𝗢𝗻𝗹𝗶𝗻𝗲 𝗿𝗲𝗰𝗲𝗻𝘁𝗲𝗺𝗲𝗻𝘁𝗲."
        elif x == enums.UserStatus.LAST_WEEK:
            return "🕒 𝗢𝗳𝗳𝗹𝗶𝗻𝗲 𝗵𝗮́ 𝘂𝗺𝗮 𝘀𝗲𝗺𝗮𝗻𝗮."
        elif x == enums.UserStatus.LONG_AGO:
            return "🔘 𝗢𝗳𝗳𝗹𝗶𝗻𝗲 𝗵𝗮́ 𝗺𝘂𝗶𝘁𝗼 𝘁𝗲𝗺𝗽𝗼."
        elif x == enums.UserStatus.OFFLINE:
            return "🔴 𝗢𝗳𝗳𝗹𝗶𝗻𝗲."
        elif x == enums.UserStatus.ONLINE:
            return "🟢 𝗢𝗻𝗹𝗶𝗻𝗲."
    except BaseException:
        return "❗ **𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗮𝗱𝗼!**"


async def get_user_info(user, already=False):
    if not already:
        user = await app.get_users(user)
    if not user.first_name:
        return ["⚠️ 𝗖𝗼𝗻𝘁𝗮 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗮", None]
    user_id = user.id
    online = await userstatus(user_id)
    username = user.username
    first_name = user.first_name
    mention = user.mention("🔗 𝗟𝗶𝗻𝗸")
    dc_id = user.dc_id
    photo_id = user.photo.big_file_id if user.photo else None
    is_gbanned = await is_gbanned_user(user_id)
    is_sudo = user_id in SUDOERS
    is_premium = user.is_premium
    body = {
        "📝 𝗡𝗼𝗺𝗲": [first_name],
        "📛 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼": [("@" + username) if username else "N/A"],
        "🆔 𝗜𝗗": user_id,
        "🌍 𝗗𝗖 𝗜𝗗": dc_id,
        "🔗 𝗠𝗲𝗻𝗰̧𝗮̃𝗼": [mention],
        "⭐ 𝗣𝗿𝗲𝗺𝗶𝘂𝗺": "Sim" if is_premium else "Não",
        "👀 𝗨́𝗹𝘁𝗶𝗺𝗮 𝘃𝗲𝘇 𝘃𝗶𝘀𝘁𝗼": online,
    }
    caption = section("👤 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼", body)
    return [caption, photo_id]


async def get_chat_info(chat):
    chat = await app.get_chat(chat)
    username = chat.username
    link = f"[🔗 𝗟𝗶𝗻𝗸](t.me/{username})" if username else "N/A"
    photo_id = chat.photo.big_file_id if chat.photo else None
    info = f"""
❅─────✧❅✦❅✧─────❅
             ✦ 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗖𝗵𝗮𝘁 ✦

➻ 🆔 𝗜𝗗 𝗱𝗼 𝗖𝗵𝗮𝘁 ‣ {chat.id}
➻ 📝 𝗡𝗼𝗺𝗲 ‣ {chat.title}
➻ 📛 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 ‣ {chat.username}
➻ 🌍 𝗗𝗖 𝗜𝗗 ‣ {chat.dc_id}
➻ 📝 𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼 ‣ {chat.description}
➻ 📋 𝗧𝗶𝗽𝗼 𝗱𝗼 𝗖𝗵𝗮𝘁 ‣ {chat.type}
➻ ✅ 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗱𝗼 ‣ {chat.is_verified}
➻ 🚫 𝗥𝗲𝘀𝘁𝗿𝗶𝘁𝗼 ‣ {chat.is_restricted}
➻ 👑 𝗖𝗿𝗶𝗮𝗱𝗼𝗿 ‣ {chat.is_creator}
➻ ⚠️ 𝗦𝗰𝗮𝗺 ‣ {chat.is_scam}
➻ 🤥 𝗙𝗮𝗸𝗲 ‣ {chat.is_fake}
➻ 👥 𝗠𝗲𝗺𝗯𝗿𝗼𝘀 ‣ {chat.members_count}
➻ 🔗 𝗟𝗶𝗻𝗸 ‣ {link}

❅─────✧❅✦❅✧─────❅"""

    return info, photo_id


@app.on_message(filters.command("info"))
async def info_func(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) == 1:
        user = message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user_input = message.text.split(None, 1)[1]
        if user_input.isdigit():
            user = int(user_input)
        elif user_input.startswith("@"):
            user = user_input
        else:
            return await message.reply_text(
                "⚠️ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝗜𝗗 𝗼𝘂 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗼𝘂 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀."
            )

    m = await message.reply_text("⏳ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...")

    try:
        info_caption, photo_id = await get_user_info(user)
    except Exception as e:
        return await m.edit(str(e))

    if not photo_id:
        return await m.edit(info_caption, disable_web_page_preview=True)
    photo = await app.download_media(photo_id)

    await message.reply_photo(photo, caption=info_caption, quote=False)
    await m.delete()
    os.remove(photo)


@app.on_message(filters.command("chatinfo"))
async def chat_info_func(_, message: Message):
    splited = message.text.split()
    if len(splited) == 1:
        chat = message.chat.id
        if chat == message.from_user.id:
            return await message.reply_text("**❗ Uso:** /chatinfo [USERNAME|ID]")
    else:
        chat = splited[1]
    try:
        m = await message.reply_text("⏳ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...")

        info_caption, photo_id = await get_chat_info(chat)
        if not photo_id:
            return await m.edit(info_caption, disable_web_page_preview=True)

        photo = await app.download_media(photo_id)
        await message.reply_photo(photo, caption=info_caption, quote=False)

        await m.delete()
        os.remove(photo)
    except Exception as e:
        await m.edit(e)


__MODULE__ = "ℹ️ 𝗜𝗻𝗳𝗼"
__HELP__ = """
**ℹ️ 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲 𝗖𝗵𝗮𝘁:**

• `/info`: 𝗢𝗯𝘁𝗲𝗺 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼. 𝗡𝗼𝗺𝗲, 𝗜𝗗, 𝗲 𝗺𝗮𝗶𝘀.
• `/chatinfo [𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘|𝗜𝗗]`: 𝗢𝗯𝘁𝗲𝗺 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗼 𝗰𝗵𝗮𝘁. 𝗡𝗼𝗺𝗲, 𝗺𝗲𝗺𝗯𝗿𝗼𝘀, 𝗲 𝗺𝗮𝗶𝘀.
"""
