import datetime
from re import findall

from Cecilia import app
from Cecilia.misc import SUDOERS
from Cecilia.utils.database import is_gbanned_user
from Cecilia.utils.functions import check_format, extract_text_and_keyb
from Cecilia.utils.keyboard import ikb
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.types import (
    Chat,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from utils import (
    del_welcome,
    get_welcome,
    set_welcome,
)
from utils.error import capture_err
from utils.permissions import admins_only
from .notes import extract_urls


async def handle_new_member(member, chat):
    try:
        if member.id in SUDOERS:
            return
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"{member.mention} 𝗳𝗼𝗶 𝗯𝗮𝗻𝗶𝗱𝗼 𝗴𝗹𝗼𝗯𝗮𝗹𝗺𝗲𝗻𝘁𝗲, 𝗲 𝗳𝗼𝗶 𝗿𝗲𝗺𝗼𝘃𝗶𝗱𝗼. ❌\n𝗦𝗲 𝘃𝗼𝗰̂𝗲̂ 𝗮𝗰𝗵𝗮 𝗾𝘂𝗲 𝗶𝘀𝘀𝗼 𝗲́ 𝘂𝗺 𝗲𝗻𝗴𝗮𝗻𝗼, 𝗽𝗼𝗱𝗲 𝗮𝗽𝗲𝗹𝗮𝗿 𝗽𝗲𝗹𝗼 𝗯𝗮𝗻𝗶𝗺𝗲𝗻𝘁𝗼 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘀𝘂𝗽𝗼𝗿𝘁𝗲. 🛡️",
            )
            return
        if member.is_bot:
            return
        return await send_welcome_message(chat, member.id)

    except ChatAdminRequired:
        return


@app.on_chat_member_updated(filters.group, group=6)
@capture_err
async def welcome(_, user: ChatMemberUpdated):
    if not (
            user.new_chat_member
            and user.new_chat_member.status not in {CMS.RESTRICTED}
            and not user.old_chat_member
    ):
        return

    member = user.new_chat_member.user if user.new_chat_member else user.from_user
    chat = user.chat
    return await handle_new_member(member, chat)


async def send_welcome_message(chat: Chat, user_id: int, delete: bool = False):
    welcome, raw_text, file_id = await get_welcome(chat.id)

    if not raw_text:
        return
    text = raw_text
    keyb = None
    if findall(r"\[.+\,.+\]", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)
    u = await app.get_users(user_id)
    if "{GROUPNAME}" in text:
        text = text.replace("{GROUPNAME}", f"𝗚𝗿𝘂𝗽𝗼 {chat.title} 🏠")
    if "{NAME}" in text:
        text = text.replace("{NAME}", f"𝗕𝗲𝗺-𝘃𝗶𝗻𝗱𝗼(a), {u.mention}! 👋")
    if "{ID}" in text:
        text = text.replace("{ID}", f"`{user_id}` 🆔")
    if "{FIRSTNAME}" in text:
        text = text.replace("{FIRSTNAME}", f"𝗢𝗶, {u.first_name}! 😊")
    if "{SURNAME}" in text:
        sname = u.last_name or "𝗦𝗲𝗺 𝘀𝗼𝗯𝗿𝗲𝗻𝗼𝗺𝗲"
        text = text.replace("{SURNAME}", sname)
    if "{USERNAME}" in text:
        susername = u.username or "𝗦𝗲𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼"
        text = text.replace("{USERNAME}", f"@{susername} 🌀")
    if "{DATE}" in text:
        DATE = datetime.datetime.now().strftime("%Y-%m-%d")
        text = text.replace("{DATE}", f"𝗗𝗮𝘁𝗮: {DATE} 📅")
    if "{WEEKDAY}" in text:
        WEEKDAY = datetime.datetime.now().strftime("%A")
        text = text.replace("{WEEKDAY}", f"𝗗𝗶𝗮 𝗱𝗮 𝘀𝗲𝗺𝗮𝗻𝗮: {WEEKDAY} 📆")
    if "{TIME}" in text:
        TIME = datetime.datetime.now().strftime("%H:%M:%S")
        text = text.replace("{TIME}", f"𝗛𝗼𝗿𝗮́𝗿𝗶𝗼: {TIME} 🕒 UTC")

    if welcome == "Text":
        m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
    elif welcome == "Photo":
        m = await app.send_photo(
            chat.id,
            photo=file_id,
            caption=text,
            reply_markup=keyb,
        )
    else:
        m = await app.send_animation(
            chat.id,
            animation=file_id,
            caption=text,
            reply_markup=keyb,
        )


@app.on_message(filters.command("setwelcome") & ~filters.private)
@admins_only("can_change_info")
async def set_welcome_func(_, message):
    usage = "𝗩𝗼𝗰𝗲̂ 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗿 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗰𝗼𝗺 𝘁𝗲𝘅𝘁𝗼, 𝗴𝗶𝗳 𝗼𝘂 𝗳𝗼𝘁𝗼 𝗽𝗮𝗿𝗮 𝘀𝗲𝘁𝗮́-𝗹𝗮 𝗰𝗼𝗺𝗼 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮𝘀.\n\n𝗡𝗼𝘁𝗮: 𝗰𝗮𝗽𝘁𝗶𝗼𝗻 𝗲́ 𝗿𝗲𝗾𝘂𝗶𝘀𝗶𝘁𝗮 𝗽𝗮𝗿𝗮 𝗴𝗶𝗳 𝗲 𝗳𝗼𝘁𝗼."
    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="𝗠𝗮𝗶𝘀 𝗔𝗷𝘂𝗱𝗮 ❓",
                    url=f"t.me/{app.username}?start=greetings",
                )
            ],
        ]
    )
    replied_message = message.reply_to_message
    chat_id = message.chat.id
    try:
        if not replied_message:
            await message.reply_text(usage, reply_markup=key)
            return
        if replied_message.animation:
            welcome = "Animation"
            file_id = replied_message.animation.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.photo:
            welcome = "Photo"
            file_id = replied_message.photo.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.text:
            welcome = "Text"
            file_id = None
            text = replied_message.text
            raw_text = text.markdown
        if replied_message.reply_markup and not findall(r"\[.+\,.+\]", raw_text):
            urls = extract_urls(replied_message.reply_markup)
            if urls:
                response = "\n".join(
                    [f"{name}=[{text}, {url}]" for name, text, url in urls]
                )
                raw_text = raw_text + response
        raw_text = await check_format(ikb, raw_text)
        if raw_text:
            await set_welcome(chat_id, welcome, raw_text, file_id)
            return await message.reply_text(
                "𝗠𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮𝘀 𝗳𝗼𝗶 𝗰𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗱𝗮 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼! 🎉"
            )
        else:
            return await message.reply_text(
                "𝗙𝗼𝗿𝗺𝗮𝘁𝗮𝗰̧𝗮̃𝗼 𝗲𝗿𝗿𝗮𝗱𝗮, 𝘃𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗮 𝘀𝗲𝗰̧𝗮𝗼 𝗱𝗲 𝗮𝗷𝘂𝗱𝗮.\n\n**𝗨𝘀𝗮𝗴𝗲:**\n𝗧𝗲𝘅𝘁𝗼: `𝗧𝗲𝘅𝘁𝗼`\n𝗧𝗲𝘅𝘁𝗼 + 𝗕𝗼𝘁𝗼̃𝗲𝘀: `𝗧𝗲𝘅𝘁𝗼 ~ 𝗕𝗼𝘁𝗼̃𝗲𝘀`",
                reply_markup=key,
            )
    except UnboundLocalError:
        return await message.reply_text(
            "**𝗔𝗽𝗲𝗻𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗱𝗲 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮𝘀 𝗲𝗺 𝘁𝗲𝘅𝘁𝗼, 𝗴𝗶𝗳 𝗲 𝗳𝗼𝘁𝗼 𝘀𝗮̃𝗼 𝘀𝘂𝗽𝗼𝗿𝘁𝗮𝗱𝗮𝘀. 📢**"
        )


@app.on_message(filters.command(["delwelcome", "deletewelcome"]) & ~filters.private)
@admins_only("can_change_info")
async def del_welcome_func(_, message):
    chat_id = message.chat.id
    await del_welcome(chat_id)
    await message.reply_text("𝗠𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮 𝗳𝗼𝗶 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮. 🗑️")


@app.on_message(filters.command("getwelcome") & ~filters.private)
@admins_only("can_change_info")
async def get_welcome_func(_, message):
    chat = message.chat
    welcome, raw_text, file_id = await get_welcome(chat.id)
    if not raw_text:
        return await message.reply_text(
            "𝗡𝗲𝗻𝗵𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮 𝗲𝘀𝘁𝗮́ 𝗰𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗱𝗮. ⚠️")
    if not message.from_user:
        return await message.reply_text(
            "𝗩𝗼𝗰𝗲̂ 𝗲́ 𝗮𝗻𝗼̂𝗻𝗶𝗺𝗼, 𝗻𝗮̃𝗼 𝗲́ 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗲𝗻𝘃𝗶𝗮𝗿 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮. 🕵️")

    await send_welcome_message(chat, message.from_user.id)

    await message.reply_text(
        f'𝗠𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗕𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮: {welcome}\n\n𝗜𝗗 𝗱𝗼 𝗔𝗿𝗾𝘂𝗶𝘃𝗼: `{file_id}`\n\n`{raw_text.replace("`", "")}`'
    )


__MODULE__ = "🙋𝗕𝗼𝗮𝘀-𝗩𝗶𝗻𝗱𝗮𝘀"
__HELP__ = """
/setwelcome - 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗰𝗼𝗺 𝗳𝗼𝗿𝗺𝗮𝘁𝗮𝗰̧𝗮̃𝗼 𝗰𝗼𝗿𝗿𝗲𝘁𝗮 𝗽𝗮𝗿𝗮 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮𝘀.\n
/delwelcome - 𝗘𝘅𝗰𝗹𝘂𝗶𝗿 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮.\n/getwelcome - 𝗢𝗯𝘁𝗲𝗿 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮.

**𝗖𝗢𝗡𝗙𝗜𝗚𝗨𝗥𝗔𝗖̧𝗔̃𝗢_𝗕𝗢𝗔𝗦_𝗩𝗜𝗡𝗗𝗔 ->**

**𝗣𝗮𝗿𝗮 𝘀𝗲𝘁𝗮𝗿 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗼𝘂 𝗴𝗶𝗳 𝗰𝗼𝗺𝗼 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮, 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗲 𝘀𝘂𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗯𝗼𝗮𝘀-𝘃𝗶𝗻𝗱𝗮 𝗰𝗼𝗺𝗼 𝗰𝗮𝗽𝘁𝗶𝗼𝗻 𝗽𝗮𝗿𝗮 𝗳𝗼𝘁𝗼 𝗼𝘂 𝗴𝗶𝗳. 𝗔 𝗰𝗮𝗽𝘁𝗶𝗼𝗻 𝗱𝗲𝘃𝗲 𝗲𝘀𝘁𝗮𝗿 𝗻𝗼 𝗳𝗼𝗿𝗺𝗮𝘁𝗼 𝗮𝗯𝗮𝗶𝘅𝗼.**

𝗣𝗮𝗿𝗮 𝘁𝗲𝘅𝘁𝗼, 𝗯𝗮𝘀𝘁𝗮 𝗲𝗻𝘃𝗶𝗮𝗿 𝗼 𝘁𝗲𝘅𝘁𝗼. 𝗘𝗺 𝘀𝗲𝗴𝘂𝗶𝗱𝗮, 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗰𝗼𝗺 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼.

𝗢 𝗳𝗼𝗿𝗺𝗮𝘁𝗼 𝗱𝗲𝘃𝗲 𝗲𝘀𝘁𝗮𝗿 𝗰𝗼𝗺𝗼 𝗮𝗯𝗮𝗶𝘅𝗼:

**𝗢𝗹𝗮́** {NAME} [{ID}] 𝗕𝗲𝗺-𝘃𝗶𝗻𝗱𝗼(a) 𝗮𝗼 {GROUPNAME}

~ #𝗢 𝘀𝗲𝗽𝗮𝗿𝗮𝗱𝗼𝗿 (~) 𝗱𝗲𝘃𝗲 𝗲𝘀𝘁𝗮𝗿 𝗲𝗻𝘁𝗿𝗲 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗲 𝗼𝘀 𝗯𝗼𝘁𝗼̃𝗲𝘀, 𝗿𝗲𝗺𝗼𝘃𝗮 𝗲𝘀𝘁𝗲 𝗰𝗼𝗺𝗲𝗻𝘁𝗮́𝗿𝗶𝗼 𝘁𝗮𝗺𝗯𝗲́𝗺.

Button=[𝗣𝗮́𝗴𝗶𝗻𝗮, 𝗵𝘁𝘁𝗽𝘀://𝘀𝗲𝘂𝘀𝗶𝘁𝗲.𝗰𝗼𝗺]
Button2=[𝗚𝗶𝘁𝗛𝘂𝗯, 𝗵𝘁𝘁𝗽𝘀://𝗴𝗶𝘁𝗵𝘂𝗯.𝗰𝗼𝗺]
**𝗡𝗢𝗧𝗔𝗦 ->**

𝗖𝗼𝗻𝗳𝗲𝗿𝗲 𝗼 /markdownhelp 𝗽𝗮𝗿𝗮 𝗺𝗮𝗶𝘀 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗳𝗼𝗿𝗺𝗮𝘁𝗮𝗰̧𝗮̃𝗼𝘀 𝗲 𝗼𝘂𝘁𝗿𝗮𝘀 𝘀𝗶𝗻𝘁𝗮𝘅𝗲𝘀.
"""
