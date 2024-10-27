import re

from WinxMusic import app
from WinxMusic.utils.database import (
    deleteall_filters,
    get_filters_names,
    save_filter,
)
from WinxMusic.utils.functions import (
    check_format,
    get_data_and_name,
)
from WinxMusic.utils.keyboard import ikb
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup, Message, CallbackQuery,
)

from utils.error import capture_err
from utils.permissions import admins_only, member_permissions
from .notes import extract_urls


@app.on_message(filters.command("filter") & ~filters.private & ~BANNED_USERS)
@admins_only("can_change_info")
async def save_filters(_, message: Message):
    try:
        if len(message.command) < 2:
            return await message.reply_text(
                "**𝙐𝙨𝙤:**\nResponda a uma mensagem com /filter [NOME_DO_FILTRO] [CONTEÚDO] para definir um novo filtro."
            )
        replied_message = message.reply_to_message
        if not replied_message:
            replied_message = message
        data, name = await get_data_and_name(replied_message, message)
        if len(name) < 2:
            return await message.reply_text(
                f"𝗣𝗮𝗿𝗮 𝗼 𝗳𝗶𝗹𝘁𝗿𝗼, {name} 𝗱𝗲𝘃𝗲 𝘁𝗲𝗿 𝗺𝗮𝗶𝘀 𝗱𝗲 𝟮 𝗽𝗮𝗹𝗮𝘃𝗿𝗮𝘀."
            )
        if data == "error":
            return await message.reply_text(
                "**𝙐𝙨𝙤:**\n__/filter [NOME_DO_FILTRO] [CONTEÚDO]__\n`-----------OU-----------`\nResponda a uma mensagem com. \n/filter [NOME_DO_FILTRO]."
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
        if replied_message.reply_markup and not re.findall(r"\[.+\,.+\]", data):
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
                    "**𝗙𝗼𝗿𝗺𝗮𝘁𝗮𝗰̧𝗮̃𝗼 𝗲𝗿𝗿𝗮𝗱𝗮, 𝗰𝗼𝗻𝗳𝗶𝗿𝗮 𝗮 𝘀𝗲𝗰̧𝗮̃𝗼 𝗱𝗲 𝗮𝗷𝘂𝗱𝗮.**"
                )
        name = name.replace("_", " ")
        _filter = {
            "type": _type,
            "data": data,
            "file_id": file_id,
        }

        chat_id = message.chat.id
        await save_filter(chat_id, name, _filter)
        return await message.reply_text(f"__**𝗙𝗶𝗹𝘁𝗿𝗼 {name} salvo com sucesso.**__")
    except UnboundLocalError:
        return await message.reply_text(
            "**𝗠𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗶𝗱𝗮 𝗶𝗻𝗮𝗰𝗲𝘀𝘀𝗶́𝘃𝗲𝗹.\nReenviar a mensagem e tente novamente.**"
        )


@app.on_message(filters.command("filters") & ~filters.private & ~BANNED_USERS)
@capture_err
async def get_filterss(_, message: Message):
    _filters = await get_filters_names(message.chat.id)
    if not _filters:
        return await message.reply_text("**𝗡𝗮̃𝗼 𝗵𝗮́ 𝗳𝗶𝗹𝘁𝗿𝗼𝘀 𝗻𝗼 𝗰𝗵𝗮𝘁.**")
    _filters.sort()
    msg = f"𝗟𝗶𝘀𝘁𝗮 𝗱𝗲 𝗳𝗶𝗹𝘁𝗿𝗼𝘀 𝗻𝗼 **{message.chat.title}** :\n"
    for _filter in _filters:
        msg += f"**-** `{_filter}`\n"
    await message.reply_text(msg)


@app.on_message(filters.command("stopall") & ~filters.private & ~BANNED_USERS)
@admins_only("can_change_info")
async def stop_all(_, message: Message):
    _filters = await get_filters_names(message.chat.id)
    if not _filters:
        await message.reply_text("**𝗡𝗮̃𝗼 𝗵𝗮́ 𝗳𝗶𝗹𝘁𝗿𝗼𝘀 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁.**")
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("𝗦𝗶𝗺, 𝗳𝗮𝘇𝗮 𝗶𝘀𝘀𝗼", callback_data="stop_yes"),
                    InlineKeyboardButton("𝗡𝗮̃𝗼, 𝗻𝗮̃𝗼 𝗳𝗮𝘇𝗮 𝗶𝘀𝘀𝗼", callback_data="stop_no"),
                ]
            ]
        )
        await message.reply_text(
            "**𝗩𝗼𝗰𝗲̂ 𝘁𝗲𝗺 𝗰𝗲𝗿𝘁𝗲𝘇𝗮 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗱𝗲𝗹𝗲𝘁𝗮𝗿 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗳𝗶𝗹𝘁𝗿𝗼𝘀 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁 𝗽𝗮𝗿𝗮 𝘀𝗲𝗺𝗽𝗿𝗲?**",
            reply_markup=keyboard,
        )


@app.on_callback_query(filters.regex("stop_(.*)") & ~BANNED_USERS)
async def stop_all_cb(_, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    from_user = callback_query.from_user
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_change_info"
    if permission not in permissions:
        return await callback_query.answer(
            f"𝗩𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝗽𝗼𝘀𝘀𝘂𝗶 𝗮 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗻𝗲𝗰𝗲𝘀𝘀𝗮́𝗿𝗶𝗮.\n Permissão: {permission}",
            show_alert=True,
        )
    input = callback_query.data.split("_", 1)[1]
    if input == "yes":
        stoped_all = await deleteall_filters(chat_id)
        if stoped_all:
            return await callback_query.message.edit(
                "**𝗧𝗼𝗱𝗼𝘀 𝗼𝘀 𝗳𝗶𝗹𝘁𝗿𝗼𝘀 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗼𝘀 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁.**"
            )
    if input == "no":
        await callback_query.message.reply_to_message.delete()
        await callback_query.message.delete()


__MODULE__ = "🔍 𝗙𝗶𝗹𝘁𝗿𝗼𝘀"
__HELP__ = """
**🗃️ Comandos de Filtros:**

• /filters - **𝗢𝗯𝘁𝗲́𝗺 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗳𝗶𝗹𝘁𝗿𝗼𝘀 𝗻𝗼 𝗰𝗵𝗮𝘁.**

• /filter [𝗡𝗢𝗠𝗘_𝗗𝗢_𝗙𝗜𝗟𝗧𝗥𝗢] - **𝗦𝗮𝗹𝘃𝗮 𝘂𝗺 𝗳𝗶𝗹𝘁𝗿𝗼** (responda a uma mensagem).

📎 **Tipos de Filtros Suportados:**
Texto, Animação, Foto, Documento, Vídeo, Notas de Vídeo, Áudio, Voz.

✨ **Dica:** Para usar mais palavras em um filtro, utilize:
`/filter Oi_tudo_bem` para filtrar "Oi tudo bem".

• /stop [𝗡𝗢𝗠𝗘_𝗗𝗢_𝗙𝗜𝗟𝗧𝗥𝗢] - **𝗣𝗮𝗿𝗮 𝘂𝗺 𝗳𝗶𝗹𝘁𝗿𝗼.**

• /stopall - **𝗗𝗲𝗹𝗲𝘁𝗮 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗳𝗶𝗹𝘁𝗿𝗼𝘀 𝗱𝗲 𝘂𝗺 𝗰𝗵𝗮𝘁 (𝗽𝗲𝗿𝗺𝗮𝗻𝗲𝗻𝘁𝗲𝗺𝗲𝗻𝘁𝗲).**

📐 **Formato Avançado:**
Você pode usar markdown ou HTML para salvar o texto também. Consulte /markdownhelp para mais informações sobre formatações e outras sintaxes.
"""
