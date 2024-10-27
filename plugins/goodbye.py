import datetime
from re import findall

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import is_gbanned_user
from WinxMusic.utils.functions import check_format, extract_text_and_keyb
from WinxMusic.utils.keyboard import ikb
from pyrogram import filters, Client
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from utils import (
    del_goodbye,
    get_goodbye,
    set_goodbye,
    is_greetings_on,
    set_greetings_on,
    set_greetings_off,
)
from utils.error import capture_err
from utils.permissions import adminsOnly
from .notes import extract_urls


async def handle_left_member(member, chat: Chat):
    try:
        if member.id in SUDOERS:
            return
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"{member.mention} 𝗳𝗼𝗶 𝗯𝗮𝗻𝗶𝗱𝗼 𝗴𝗹𝗼𝗯𝗮𝗹𝗺𝗲𝗻𝘁𝗲 𝗲 𝗿𝗲𝗺𝗼𝘃𝗶𝗱𝗼."
                + " 𝗦𝗲 𝗮𝗰𝗵𝗮𝗿 𝗾𝘂𝗲 𝗲𝘀𝘁𝗲 𝗲́ 𝘂𝗺 𝗲𝗿𝗿𝗼 𝗱𝗲 𝗯𝗮𝗻𝗶𝗺𝗲𝗻𝘁𝗼, 𝗽𝗲𝗱𝗶𝗺𝗼𝘀 𝗾𝘂𝗲 𝗳𝗮𝗰̧𝗮 𝘂𝗺𝗮 𝗮𝗽𝗲𝗹𝗮𝗰̧𝗮̃𝗼 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝗮𝗷𝘂𝗱𝗮.",
            )
            return
        if member.is_bot:
            return
        return await send_left_message(chat, member.id)

    except ChatAdminRequired:
        return


@app.on_message(filters.left_chat_member & filters.group, group=6)
@capture_err
async def goodbye(_, message: Message):
    if message.from_user:
        member = await app.get_users(message.from_user.id)
        chat = message.chat
        return await handle_left_member(member, chat)


async def send_left_message(chat: Chat, user_id: int, delete: bool = False):
    is_on = await is_greetings_on(chat.id, "goodbye")

    if not is_on:
        return

    goodbye, raw_text, file_id = await get_goodbye(chat.id)

    if not raw_text:
        return

    text = raw_text
    keyb = None

    if findall(r"\[.+\,.+\]", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)

    u = await app.get_users(user_id)

    replacements = {
        "{NAME}": u.mention,
        "{ID}": f"`{user_id}`",
        "{FIRSTNAME}": u.first_name,
        "{GROUPNAME}": chat.title,
        "{SURNAME}": u.last_name or "None",
        "{USERNAME}": u.username or "None",
        "{DATE}": datetime.datetime.now().strftime("%Y-%m-%d"),
        "{WEEKDAY}": datetime.datetime.now().strftime("%A"),
        "{TIME}": datetime.datetime.now().strftime("%H:%M:%S") + " UTC",
    }

    for placeholder, value in replacements.items():
        if placeholder in text:
            text = text.replace(placeholder, value)

    if goodbye == "Text":
        m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
    elif goodbye == "Photo":
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


@app.on_message(filters.command("setgoodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def set_goodbye_func(_, message: Message):
    usage = "𝗩𝗼𝗰𝗲̂ 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗿 𝗮 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼, 𝗴𝗶𝗳 𝗼𝘂 𝗳𝗼𝘁𝗼 𝗽𝗮𝗿𝗮 𝗱𝗲𝗳𝗶𝗻𝗶-𝗹𝗼 𝗰𝗼𝗺𝗼 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮.\n\n𝗢𝗯𝘀: 𝗲́ 𝗻𝗲𝗰𝗲𝘀𝘀𝗮́𝗿𝗶𝗼 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝘂𝗺𝗮 𝗹𝗲𝗴𝗲𝗻𝗱𝗮 𝗽𝗮𝗿𝗮 𝗴𝗶𝗳 𝗲 𝗳𝗼𝘁𝗼."
    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Mais Ajuda",
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
            goodbye = "Animation"
            file_id = replied_message.animation.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.photo:
            goodbye = "Photo"
            file_id = replied_message.photo.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.text:
            goodbye = "Text"
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
            await set_goodbye(chat_id, goodbye, raw_text, file_id)
            return await message.reply_text(
                "𝗔 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮 𝗳𝗼𝗶 𝗱𝗲𝗳𝗶𝗻𝗶𝗱𝗮 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼."
            )
        else:
            return await message.reply_text(
                "𝗙𝗼𝗿𝗺𝗮𝘁𝗮𝗰̧𝗮̃𝗼 𝗲𝗿𝗿𝗮𝗱𝗮, 𝘃𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗮 𝘀𝗲𝗰̧𝗮̃𝗼 𝗱𝗲 𝗮𝗷𝘂𝗱𝗮.\n\n**𝗨𝘀𝗮𝗴𝗲:**\n𝗧𝗲𝘅𝘁𝗼: `Texto`\n𝗧𝗲𝘅𝘁𝗼 + 𝗯𝗼𝘁𝗼̃𝗲𝘀: `Texto ~ Botões`",
                reply_markup=key,
            )
    except UnboundLocalError:
        return await message.reply_text(
            "**𝗔𝗽𝗲𝗻𝗮𝘀 𝗧𝗲𝘅𝘁𝗼, 𝗚𝗶𝗳 𝗲 𝗙𝗼𝘁𝗼 𝘀𝗮̃𝗼 𝗮𝗽𝗼𝗶𝗮𝗱𝗼𝘀 𝗽𝗮𝗿𝗮 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮.**"
        )


@app.on_message(filters.command(["delgoodbye", "deletegoodbye"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_goodbye_func(_, message: Message):
    chat_id = message.chat.id
    await del_goodbye(chat_id)
    await message.reply_text("𝗠𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮 𝗳𝗼𝗶 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗮 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼.")


@app.on_message(filters.command("goodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def goodbye(client: Client, message: Message):
    command = message.text.split()

    if len(command) == 1:
        return await get_goodbye_func(client, message)

    if len(command) == 2:
        action = command[1].lower()
        if action in ["on", "enable", "y", "yes", "true", "t"]:
            success = await set_greetings_on(message.chat.id, "goodbye")
            if success:
                await message.reply_text(
                    "𝗔𝗴𝗼𝗿𝗮 𝗱𝗶𝗿𝗲𝗶 𝗮𝗱𝗲𝘂𝘀 𝗮𝗼𝘀 𝗺𝗲𝗺𝗯𝗿𝗼𝘀 𝗾𝘂𝗲 𝘀𝗮𝗶𝗿𝗲𝗺!"
                )
            else:
                await message.reply_text(
                    "𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗮𝘁𝗶𝘃𝗮𝗿 𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮.")

        elif action in ["off", "disable", "n", "no", "false", "f"]:
            success = await set_greetings_off(message.chat.id, "goodbye")
            if success:
                await message.reply_text("𝗙𝗶𝗰𝗮𝗿𝗲𝗶 𝗲𝗺 𝘀𝗶𝗹𝗲̂𝗻𝗰𝗶𝗼 𝗾𝘂𝗮𝗻𝗱𝗼 𝗮𝗹𝗴𝘂𝗲𝗺 𝘀𝗮𝗶𝗿.")
            else:
                await message.reply_text(
                    "𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗿 𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮.")

        else:
            await message.reply_text(
                "𝗖𝗼𝗺𝗮𝗻𝗱𝗼 𝗶𝗻𝘃𝗮́𝗹𝗶𝗱𝗼. 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿 𝘂𝘀𝗲:\n"
                "/goodbye - 𝗣𝗮𝗿𝗮 𝗿𝗲𝗰𝗲𝗯𝗲𝗿 𝗮 𝘀𝘂𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮\n"
                "/goodbye [on, y, true, enable, t] - 𝗽𝗮𝗿𝗮 𝗮𝘁𝗶𝘃𝗮𝗿 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮\n"
                "/goodbye [off, n, false, disable, f, no] - 𝗽𝗮𝗿𝗮 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗿 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮\n"
                "/delgoodbye ou /deletegoodbye para deletar a mensagem de despedida e desativá-la"
            )
    else:
        await message.reply_text(
            "𝗖𝗼𝗺𝗮𝗻𝗱𝗼 𝗶𝗻𝘃𝗮́𝗹𝗶𝗱𝗼. 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿 𝘂𝘀𝗲:\n"
            "/goodbye - 𝗣𝗮𝗿𝗮 𝗿𝗲𝗰𝗲𝗯𝗲𝗿 𝗮 𝘀𝘂𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮\n"
            "/goodbye [on, y, true, enable, t] - 𝗽𝗮𝗿𝗮 𝗮𝘁𝗶𝘃𝗮𝗿 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮\n"
            "/goodbye [off, n, false, disable, f, no] - 𝗽𝗮𝗿𝗮 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗿 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮\n"
            "/delgoodbye ou /deletegoodbye para deletar a mensagem de despedida e desativá-la"
        )


async def get_goodbye_func(_, message: Message):
    chat = message.chat
    goodbye, raw_text, file_id = await get_goodbye(chat.id)
    if not raw_text:
        return await message.reply_text(
            "𝗘𝘀𝗾𝘂𝗲𝗰𝗲𝘂 𝗱𝗲 𝘀𝗲𝘁𝗮𝗿 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮?"
        )
    if not message.from_user:
        return await message.reply_text(
            "𝗩𝗼𝗰𝗲̂ 𝗲́ 𝗮𝗻𝗼̂𝗻𝗶𝗺𝗼, 𝗻𝗮̃𝗼 𝗲́ 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗲𝗻𝘃𝗶𝗮𝗿 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮.")

    await send_left_message(chat, message.from_user.id)
    is_grt = await is_greetings_on(chat.id, "goodbye")
    text = None
    if is_grt:
        text = "𝗔𝘁𝗶𝘃𝗮𝗱𝗼"
    else:
        text = "𝗗𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗱𝗼"
    await message.reply_text(
        f'𝗔𝘁𝘂𝗮𝗹𝗺𝗲𝗻𝘁𝗲 𝗲𝘀𝘁𝗼𝘂 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗻𝗱𝗼-𝗺𝗲 𝗱𝗲 𝗺𝗲𝗺𝗯𝗿𝗼𝘀: {text}\n𝗠𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮: {goodbye}\n\n𝗙𝗶𝗹𝗲 𝗜𝗗: `{file_id}`\n\n`{raw_text.replace("`", "")}`',
    )


__MODULE__ = "👋𝗗𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮"
__HELP__ = """
𝗔𝗷𝘂𝗱𝗮 𝗽𝗮𝗿𝗮 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮:

/setgoodbye - 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗲𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗰𝗼𝗻𝘁𝗲𝗻𝗱𝗼 𝗮 𝗳𝗼𝗿𝗺𝗮𝘁𝗮𝗰̧𝗮̃𝗼 𝗰𝗼𝗿𝗿𝗲𝘁𝗮 𝗽𝗮𝗿𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮.

/goodbye - 𝗣𝗮𝗿𝗮 𝗲𝘅𝗶𝗯𝗶𝗿 𝗮 𝘀𝘂𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮

/goodbye  [𝗼𝗻, 𝘆, 𝘁𝗿𝘂𝗲, 𝗲𝗻𝗮𝗯𝗹𝗲, 𝘁] - 𝗽𝗮𝗿𝗮 𝗮𝘁𝗶𝘃𝗮𝗿 𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮

/goodbye [𝗼𝗳𝗳, 𝗻, 𝗳𝗮𝗹𝘀𝗲, 𝗱𝗶𝘀𝗮𝗯𝗹𝗲, 𝗳, 𝗻𝗼] - 𝗽𝗮𝗿𝗮 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗿 𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮

/delgoodbye ou /deletegoodbye - 𝗽𝗮𝗿𝗮 𝗱𝗲𝗹𝗲𝘁𝗮𝗿 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮 𝗲 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮́-𝗹𝗮

**Definir Despedida ->**

𝗣𝗮𝗿𝗮 𝘀𝗲𝘁𝗮𝗿 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗼𝘂 𝗴𝗶𝗳 𝗰𝗼𝗺𝗼 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮, 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗲 𝘀𝘂𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮 𝗰𝗼𝗺𝗼 𝗹𝗲𝗴𝗲𝗻𝗱𝗮 𝗻𝗮 𝗳𝗼𝘁𝗼 𝗼𝘂 𝗴𝗶𝗳. 𝗔 𝗹𝗲𝗴𝗲𝗻𝗱𝗮 𝗱𝗲𝘃𝗲 𝗲𝘀𝘁𝗮́ 𝗻𝗼 𝗳𝗼𝗿𝗺𝗮𝘁𝗼 𝗮𝗯𝗮𝗶𝘅𝗼.

𝗣𝗮𝗿𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗱𝗲𝘀𝗽𝗲𝗱𝗶𝗱𝗮 𝗲𝗺 𝘁𝗲𝘅𝘁𝗼, 𝗲𝗻𝘃𝗶𝗲 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗲𝗺 𝘁𝗲𝘅𝘁𝗼 𝗲 𝗲𝗻𝘁𝗮̃𝗼 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗰𝗼𝗺 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼.

𝗢 𝗳𝗼𝗿𝗺𝗮𝘁𝗼 𝗱𝗲𝘃𝗲 𝘀𝗲𝗿 𝗰𝗼𝗺𝗼 𝗼 𝗮𝗯𝗮𝗶𝘅𝗼:

𝗢𝗹𝗮́ {NAME} [{ID}], 𝘀𝗲𝗷𝗮 𝗯𝗲𝗺-𝘃𝗶𝗻𝗱𝗼 𝗮𝗼 𝗴𝗿𝘂𝗽𝗼 {GROUPNAME}

~ #𝗘𝘀𝘀𝗲 𝘀𝗲𝗽𝗮𝗿𝗮𝗱𝗼𝗿 (~) 𝗱𝗲𝘃𝗲 𝗲𝘀𝘁𝗮𝗿 𝗲𝗻𝘁𝗿𝗲 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗲 𝗼𝘀 𝗯𝗼𝘁𝗼̃𝗲𝘀. 𝗥𝗲𝗺𝗼𝘃𝗮 𝗲𝘀𝘀𝗮 𝗹𝗶𝗻𝗵𝗮 𝗮𝗼 𝘂𝘀𝗮𝗿.

Botao=[Dᴜᴄᴋ, 𝗵𝘁𝘁𝗽𝘀://𝗱𝘂𝗰𝗸𝗱𝘂𝗰𝗸𝗴𝗼.𝗰𝗼𝗺]
Botao2=[Gɪᴛʜᴜʙ, 𝗵𝘁𝘁𝗽𝘀://𝗴𝗶𝘁𝗵𝘂𝗯.𝗰𝗼𝗺]
**𝗡𝗢𝗧𝗔𝗦 ->**

𝗖𝗼𝗻𝗳𝗲𝗿𝗶𝗿 /markdownhelp 𝗽𝗮𝗿𝗮 𝘀𝗮𝗯𝗲𝗿 𝗺𝗮𝗶𝘀 𝘀𝗼𝗯𝗿𝗲 𝗳𝗼𝗿𝗺𝗮𝘁𝗮𝗰̧𝗼̃𝗲𝘀 𝗲 𝗼𝘂𝘁𝗿𝗮𝘀 𝘀𝗶𝗻𝘁𝗮𝘅𝗲𝘀.
"""
