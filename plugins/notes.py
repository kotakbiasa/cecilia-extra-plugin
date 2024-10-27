import datetime
from inspect import getfullargspec
from re import findall

from WinxMusic import app
from WinxMusic.utils.database import (
    delete_note,
    deleteall_notes,
    get_note,
    get_note_names,
    save_note,
)
from WinxMusic.utils.functions import (
    check_format,
    extract_text_and_keyb,
    get_data_and_name,
)
from WinxMusic.utils.keyboard import ikb
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from utils.error import capture_err
from utils.permissions import admins_only, member_permissions


def extract_urls(reply_markup: InlineKeyboardMarkup):
    urls = []
    if reply_markup.inline_keyboard:
        buttons = reply_markup.inline_keyboard
        for i, row in enumerate(buttons):
            for j, button in enumerate(row):
                if button.url:
                    name = (
                        "\n~\nbutton"
                        if i * len(row) + j + 1 == 1
                        else f"button{i * len(row) + j + 1}"
                    )
                    urls.append((f"{name}", button.text, button.url))
    return urls


async def eor(message: Message, **kwargs: dict):
    func = (
        (message.edit_text if message.from_user.is_self else message.reply)
        if message.from_user
        else message.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_message(filters.command("save") & filters.group & ~BANNED_USERS)
@admins_only("can_change_info")
async def save_note(_, message: Message):
    try:
        if len(message.command) < 2:
            await eor(
                message,
                text="**𝗨𝘀𝗼: 📝**\n𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗰𝗼𝗺 /save [𝗡𝗢𝗠𝗘_𝗡𝗢𝗧𝗔] 𝗽𝗮𝗿𝗮 𝘀𝗮𝗹𝘃𝗮𝗿 𝘂𝗺𝗮 𝗻𝗼𝘃𝗮 𝗻𝗼𝘁𝗮.",
            )
        else:
            replied_message = message.reply_to_message
            if not replied_message:
                replied_message = message
            data, name = await get_data_and_name(replied_message, message)
            if data == "error":
                return await message.reply_text(
                    "**𝗨𝘀𝗼: 📝**\n__/save [𝗡𝗢𝗠𝗘_𝗡𝗢𝗧𝗔] [𝗖𝗢𝗡𝗧𝗘Ú𝗗𝗢]__\n`-----------𝗢𝗨-----------`\n𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗰𝗼𝗺.\n/save [𝗡𝗢𝗠𝗘_𝗡𝗢𝗧𝗔]"
                )
            if replied_message.text:
                _type = "text"
                file_id = None
            if replied_message.sticker:
                _type = "sticker"
                file_id = replied_message.sticker.file_id
            if replied_message.animation:
                _type = "animation"
                file_id = replied_message.animation.file_id
            if replied_message.photo:
                _type = "photo"
                file_id = replied_message.photo.file_id
            if replied_message.document:
                _type = "document"
                file_id = replied_message.document.file_id
            if replied_message.video:
                _type = "video"
                file_id = replied_message.video.file_id
            if replied_message.video_note:
                _type = "video_note"
                file_id = replied_message.video_note.file_id
            if replied_message.audio:
                _type = "audio"
                file_id = replied_message.audio.file_id
            if replied_message.voice:
                _type = "voice"
                file_id = replied_message.voice.file_id
            if replied_message.reply_markup and not findall(r"\[.+\,.+\]", data):
                urls = extract_urls(replied_message.reply_markup)
                if urls:
                    response = "\n".join(
                        [f"{name}=[{text}, {url}]" for name, text, url in urls]
                    )
                    data = data + response
            if data:
                data = await check_format(ikb, data)
                if not data:
                    return await message.reply_text(
                        "**⚠️ 𝗙𝗼𝗿𝗺𝗮𝘁𝗼 𝗶𝗻𝗰𝗼𝗿𝗿𝗲𝘁𝗼, 𝘃𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗮 𝘀𝗲𝗰̧𝗮̃𝗼 𝗱𝗲 𝗮𝗷𝘂𝗱𝗮.**"
                    )
            note = {
                "type": _type,
                "data": data,
                "file_id": file_id,
            }
            chat_id = message.chat.id
            await save_note(chat_id, name, note)
            await eor(message, text=f"__**✅ 𝗡𝗼𝘁𝗮 {name} 𝘀𝗮𝗹𝘃𝗮.**__")
    except UnboundLocalError as e:
        return await message.reply_text(
            "**⚠️ 𝗔 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗶𝗱𝗮 𝗲́ 𝗶𝗻𝗮𝗰𝗲𝘀𝘀𝗶́𝘃𝗲𝗹.\n`𝗘𝗻𝗰𝗮𝗺𝗶𝗻𝗵𝗲 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗲 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲`**"
        )


@app.on_message(filters.command("notes") & filters.group & ~BANNED_USERS)
@capture_err
async def get_notes(_, message: Message):
    chat_id = message.chat.id

    _notes = await get_note_names(chat_id)

    if not _notes:
        return await eor(message, text="**📓❌ 𝗡𝗮̃𝗼 𝗵𝗮́ 𝗻𝗼𝘁𝗮𝘀 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁.**")
    _notes.sort()
    msg = f"𝗟𝗶𝘀𝘁𝗮 𝗱𝗲 𝗻𝗼𝘁𝗮𝘀 𝗲𝗺 {message.chat.title}\n"
    for note in _notes:
        msg += f"**-** `{note}`\n"
    await eor(message, text=msg)


@app.on_message(filters.command("get") & filters.group & ~BANNED_USERS)
@capture_err
async def get_one_note(_, message: Message):
    if len(message.text.split()) < 2:
        return await eor(message, text="⚠️ 𝗔𝗿𝗴𝘂𝗺𝗲𝗻𝘁𝗼𝘀 𝗶𝗻𝘃á𝗹𝗶𝗱𝗼𝘀")
    from_user = message.from_user if message.from_user else message.sender_chat
    chat_id = message.chat.id
    name = message.text.split(None, 1)[1]
    if not name:
        return
    _note = await get_note(chat_id, name)
    if not _note:
        return
    type = _note["type"]
    data = _note["data"]
    file_id = _note.get("file_id")
    keyb = None
    if data:
        if "{app.mention}" in data:
            data = data.replace("{app.mention}", app.mention)
        if "{GROUPNAME}" in data:
            data = data.replace("{GROUPNAME}", message.chat.title)
        if "{NAME}" in data:
            data = data.replace("{NAME}", message.from_user.mention)
        if "{ID}" in data:
            data = data.replace("{ID}", f"`message.from_user.id`")
        if "{FIRSTNAME}" in data:
            data = data.replace("{FIRSTNAME}", message.from_user.first_name)
        if "{SURNAME}" in data:
            sname = (
                message.from_user.last_name
                if message.from_user.last_name.last_name
                else "None"
            )
            data = data.replace("{SURNAME}", sname)
        if "{USERNAME}" in data:
            susername = (
                message.from_user.username if message.from_user.username else "None"
            )
            data = data.replace("{USERNAME}", susername)
        if "{DATE}" in data:
            DATE = datetime.datetime.now().strftime("%Y-%m-%d")
            data = data.replace("{DATE}", DATE)
        if "{WEEKDAY}" in data:
            WEEKDAY = datetime.datetime.now().strftime("%A")
            data = data.replace("{WEEKDAY}", WEEKDAY)
        if "{TIME}" in data:
            TIME = datetime.datetime.now().strftime("%H:%M:%S")
            data = data.replace("{TIME}", f"{TIME} UTC")

        if findall(r"\[.+\,.+\]", data):
            keyboard = extract_text_and_keyb(ikb, data)
            if keyboard:
                data, keyb = keyboard
    replied_message = message.reply_to_message
    if replied_message:
        replied_user = (
            replied_message.from_user
            if replied_message.from_user
            else replied_message.sender_chat
        )
        if replied_user.id != from_user.id:
            message = replied_message
    await get_reply(message, type, file_id, data, keyb)


@app.on_message(filters.regex(r"^#.+") & filters.text & filters.group & ~BANNED_USERS)
@capture_err
async def get_one_note(_, message: Message):
    from_user = message.from_user if message.from_user else message.sender_chat
    chat_id = message.chat.id
    name = message.text.replace("#", "", 1)
    if not name:
        return
    _note = await get_note(chat_id, name)
    if not _note:
        return
    type = _note["type"]
    data = _note["data"]
    file_id = _note.get("file_id")
    keyb = None
    if data:
        if "{app.mention}" in data:
            data = data.replace("{app.mention}", app.mention)
        if "{GROUPNAME}" in data:
            data = data.replace("{GROUPNAME}", message.chat.title)
        if "{NAME}" in data:
            data = data.replace("{NAME}", message.from_user.mention)
        if "{ID}" in data:
            data = data.replace("{ID}", f"`message.from_user.id`")
        if "{FIRSTNAME}" in data:
            data = data.replace("{FIRSTNAME}", message.from_user.first_name)
        if "{SURNAME}" in data:
            sname = (
                message.from_user.last_name
                if message.from_user.last_name.last_name
                else "None"
            )
            data = data.replace("{SURNAME}", sname)
        if "{USERNAME}" in data:
            susername = (
                message.from_user.username if message.from_user.username else "None"
            )
            data = data.replace("{USERNAME}", susername)
        if "{DATE}" in data:
            DATE = datetime.datetime.now().strftime("%Y-%m-%d")
            data = data.replace("{DATE}", DATE)
        if "{WEEKDAY}" in data:
            WEEKDAY = datetime.datetime.now().strftime("%A")
            data = data.replace("{WEEKDAY}", WEEKDAY)
        if "{TIME}" in data:
            TIME = datetime.datetime.now().strftime("%H:%M:%S")
            data = data.replace("{TIME}", f"{TIME} UTC")

        if findall(r"\[.+\,.+\]", data):
            keyboard = extract_text_and_keyb(ikb, data)
            if keyboard:
                data, keyb = keyboard
    replied_message = message.reply_to_message
    if replied_message:
        replied_user = (
            replied_message.from_user
            if replied_message.from_user
            else replied_message.sender_chat
        )
        if replied_user.id != from_user.id:
            message = replied_message
    await get_reply(message, type, file_id, data, keyb)


async def get_reply(message: Message, type: str, file_id: str, data: str, key_b: InlineKeyboardMarkup):
    if type == "text":
        await message.reply_text(
            text=data,
            reply_markup=key_b,
            disable_web_page_preview=True,
        )
    if type == "sticker":
        await message.reply_sticker(
            sticker=file_id,
        )
    if type == "animation":
        await message.reply_animation(
            animation=file_id,
            caption=data,
            reply_markup=key_b,
        )
    if type == "photo":
        await message.reply_photo(
            photo=file_id,
            caption=data,
            reply_markup=key_b,
        )
    if type == "document":
        await message.reply_document(
            document=file_id,
            caption=data,
            reply_markup=key_b,
        )
    if type == "video":
        await message.reply_video(
            video=file_id,
            caption=data,
            reply_markup=key_b,
        )
    if type == "video_note":
        await message.reply_video_note(
            video_note=file_id,
        )
    if type == "audio":
        await message.reply_audio(
            audio=file_id,
            caption=data,
            reply_markup=key_b,
        )
    if type == "voice":
        await message.reply_voice(
            voice=file_id,
            caption=data,
            reply_markup=key_b,
        )


@app.on_message(filters.command("delete") & filters.group & ~BANNED_USERS)
@admins_only("can_change_info")
async def del_note(_, message):
    if len(message.command) < 2:
        return await eor(message, text="**𝗨𝘀𝗼 🗑️**\n__/delete [𝗡𝗢𝗠𝗘_𝗡𝗢𝗧𝗔]__")
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await eor(message, text="**𝗨𝘀𝗼 🗑️**\n__/delete [𝗡𝗢𝗠𝗘_𝗡𝗢𝗧𝗔]__")

    chat_id = message.chat.id

    deleted = await delete_note(chat_id, name)
    if deleted:
        await eor(message, text=f"**✅ 𝗡𝗼𝘁𝗮 {name} 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼.**")
    else:
        await eor(message, text="**❌ 𝗡𝗲𝗻𝗵𝘂𝗺𝗮 𝗻𝗼𝘁𝗮 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗱𝗮.**")


@app.on_message(filters.command("deleteall") & filters.group & ~BANNED_USERS)
@admins_only("can_change_info")
async def delete_all(_, message):
    _notes = await get_note_names(message.chat.id)
    if not _notes:
        return await message.reply_text("**📓❌ 𝗡𝗮̃𝗼 𝗵𝗮́ 𝗻𝗼𝘁𝗮𝘀 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁.**")
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("YES, DO IT", callback_data="delete_yes"),
                    InlineKeyboardButton("Cancel", callback_data="delete_no"),
                ]
            ]
        )
        await message.reply_text(
            "**⚠️ 𝗧𝗲𝗺 𝗰𝗲𝗿𝘁𝗲𝘇𝗮 𝗱𝗲 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗲𝘅𝗰𝗹𝘂𝗶𝗿 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗻𝗼𝘁𝗮𝘀 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁 𝗽𝗮𝗿𝗮 𝘀𝗲𝗺𝗽𝗿𝗲?**",
            reply_markup=keyboard,
        )


@app.on_callback_query(filters.regex("delete_(.*)"))
async def delete_all_cb(_, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    from_user = callback_query.from_user
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_change_info"
    if permission not in permissions:
        return await callback_query.answer(
            f"❌ 𝗩𝗼𝗰ê 𝗻ã𝗼 𝘁𝗲𝗺 𝗮 𝗽𝗲𝗿𝗺𝗶𝘀𝘀ã𝗼 𝗻𝗲𝗰𝗲𝘀𝘀á𝗿𝗶𝗮.\n 𝗣𝗲𝗿𝗺𝗶𝘀𝘀ã𝗼: {permission}",
            show_alert=True,
        )
    input = callback_query.data.split("_", 1)[1]
    if input == "yes":
        stoped_all = await deleteall_notes(chat_id)
        if stoped_all:
            return await callback_query.message.edit(
                "**✅ 𝗧𝗼𝗱𝗮𝘀 𝗮𝘀 𝗻𝗼𝘁𝗮𝘀 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁 𝗳𝗼𝗿𝗮𝗺 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮𝘀 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼.**"
            )
    if input == "no":
        await callback_query.message.reply_to_message.delete()
        await callback_query.message.delete()


__MODULE__ = "📝𝗡𝗼𝘁𝗮𝘀"
__HELP__ = """
**𝗡𝗼𝘁𝗮𝘀:**

• `/save [𝗡𝗢𝗠𝗘_𝗡𝗢𝗧𝗔] [𝗖𝗢𝗡𝗧𝗘Ú𝗗𝗢]` 📝: 𝗦𝗮𝗹𝘃𝗮 𝘂𝗺𝗮 𝗻𝗼𝘁𝗮 𝗰𝗼𝗺 𝗼 𝗻𝗼𝗺𝗲 𝗲 𝗰𝗼𝗻𝘁𝗲ú𝗱𝗼 𝗱𝗮𝗱𝗼𝘀.
• `/notes` 📋: 𝗠𝗼𝘀𝘁𝗿𝗮 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗻𝗼𝘁𝗮𝘀 𝘀𝗮𝗹𝘃𝗮𝘀 𝗻𝗼 𝗰𝗵𝗮𝘁.
• `/get [𝗡𝗢𝗠𝗘_𝗡𝗢𝗧𝗔]` 🔍: 𝗢𝗯𝘁é𝗺 𝗼 𝗰𝗼𝗻𝘁𝗲ú𝗱𝗼 𝗱𝗲 𝘂𝗺𝗮 𝗻𝗼𝘁𝗮 𝘀𝗮𝗹𝘃𝗮.
• `/delete [𝗡𝗢𝗠𝗘_𝗡𝗢𝗧𝗔]` 🗑️: 𝗘𝘅𝗰𝗹𝘂𝗶 𝘂𝗺𝗮 𝗻𝗼𝘁𝗮 𝘀𝗮𝗹𝘃𝗮.
• `/deleteall` ⚠️: 𝗘𝘅𝗰𝗹𝘂𝗶 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗻𝗼𝘁𝗮𝘀 𝘀𝗮𝗹𝘃𝗮𝘀 𝗻𝗼 𝗰𝗵𝗮𝘁.
"""
