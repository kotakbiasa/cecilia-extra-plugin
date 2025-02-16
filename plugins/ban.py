import asyncio
from contextlib import suppress
from string import ascii_lowercase
from typing import Dict, Union

from Cecilia import app
from Cecilia.core.mongo import mongodb
from Cecilia.misc import SUDOERS
from Cecilia.utils.database import save_filter
from Cecilia.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)
from Cecilia.utils.keyboard import ikb
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    ChatPrivileges,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from utils.error import capture_err
from utils.permissions import admins_only, member_permissions

warnsdb = mongodb.warns

__MODULE__ = "🚫 𝗕𝗮𝗻"
__HELP__ = """
**Comandos de Moderação:**

- /ban - 🚷 **Banir um usuário**
- /sban - 🧹 **Apagar todas as mensagens de um usuário e bani-lo**
- /tban - ⏰ **Banir um usuário por tempo específico**
- /unban - 🔓 **Desbanir um usuário**

**Avisos e Advertências:**
- /warn - ⚠️ **Advertir um usuário**
- /swarn - 🧹 **Apagar todas as mensagens do usuário e adverti-lo**
- /rmwarns - 🗑️ **Remover todas as advertências de um usuário**
- /warns - 📋 **Mostrar advertências de um usuário**

**Ações de Remoção:**
- /kick - 🚪 **Expulsar um usuário**
- /skick - 🧹 **Apagar a mensagem e expulsar o usuário**

**Limpeza e Mensagens:**
- /purge - 🧽 **Limpar mensagens**
- /purge [n] - 🔢 **Limpar "n" mensagens a partir da mensagem respondida**
- /del - 🗑️ **Apagar mensagem respondida**

**Gerenciamento de Permissões:**
- /promote - 🏆 **Promover um membro**
- /fullpromote - 🏅 **Promover um membro com todos os direitos**
- /demote - ⚙️ **Rebaixar um membro**

**Fixação de Mensagens:**
- /pin - 📌 **Fixar uma mensagem**
- /unpin - 📍 **Desfixar uma mensagem**
- /unpinall - 📍🗑️ **Desfixar todas as mensagens**

**Silenciar e Restaurar Voz:**
- /mute - 🔇 **Silenciar um usuário**
- /tmute - ⏰🔇 **Silenciar um usuário por tempo específico**
- /unmute - 🔊 **Restaurar o som de um usuário**

**Outros Comandos:**
- /zombies - 👻 **Banir contas excluídas**
- /report | @admins | @admin - 📢 **Reportar uma mensagem aos administradores**
- /link - 🔗 **Enviar o link de convite do grupo/supergrupo**
"""


async def int_to_alpha(user_id: int) -> str:
    alphabet = list(ascii_lowercase)[:10]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def get_warns_count() -> dict:
    chats_count = 0
    warns_count = 0
    async for chat in warnsdb.find({"chat_id": {"$lt": 0}}):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> Dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    if not warns:
        return {}
    return warns["warns"]


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn

    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"warns": warnsd}},
            upsert=True,
        )
        return True
    return False


@app.on_message(filters.command(["kick", "skick"]) & ~filters.private & ~BANNED_USERS)
@admins_only("can_restrict_members")
async def kick_func(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")
    if user_id == app.id:
        return await message.reply_text(
            "❌ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗺𝗲 𝗲𝘅𝗽𝘂𝗹𝘀𝗮𝗿, 𝗺𝗮𝘀 𝗽𝗼𝘀𝘀𝗼 𝘀𝗮𝗶𝗿 𝘀𝗲 𝗱𝗲𝘀𝗲𝗷𝗮𝗿.**")
    if user_id in SUDOERS:
        return await message.reply_text(
            "👑 **𝗤𝘂𝗲𝗿 𝗺𝗲𝘀𝗺𝗼 𝗲𝘅𝗽𝘂𝗹𝘀𝗮𝗿 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲𝗹𝗲𝘃𝗮𝗱𝗼?**")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "⚠️ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗲𝘅𝗽𝘂𝗹𝘀𝗮𝗿 𝘂𝗺 𝗮𝗱𝗺𝗶𝗻. 𝗩𝗼𝗰𝗲̂ 𝗰𝗼𝗻𝗵𝗲𝗰𝗲 𝗮𝘀 𝗿𝗲𝗴𝗿𝗮𝘀, 𝗲 𝗲𝘂 𝘁𝗮𝗺𝗯𝗲́𝗺.**"
        )
    mention = (await app.get_users(user_id)).mention
    msg = f"""
**🚫 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲𝘅𝗽𝘂𝗹𝘀𝗼:** {mention}
**👤 𝗘𝘅𝗽𝘂𝗹𝘀𝗼 𝗽𝗼𝗿:** {message.from_user.mention if message.from_user else '𝗔𝗻𝗼̂𝗻𝗶𝗺𝗼'}
**📄 𝗠𝗼𝘁𝗶𝘃𝗼:** {reason or '𝗡𝗲𝗻𝗵𝘂𝗺 𝗺𝗼𝘁𝗶𝘃𝗼 𝗳𝗼𝗿𝗻𝗲𝗰𝗶𝗱𝗼'}"""
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)


# Ban members


@app.on_message(
    filters.command(["ban", "sban", "tban"]) & ~filters.private & ~BANNED_USERS
)
@admins_only("can_restrict_members")
async def ban_func(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")
    if user_id == app.id:
        return await message.reply_text(
            "❌ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗺𝗲 𝗯𝗮𝗻𝗶𝗿, 𝗺𝗮𝘀 𝗽𝗼𝘀𝘀𝗼 𝘀𝗮𝗶𝗿 𝘀𝗲 𝗾𝘂𝗶𝘀𝗲𝗿.**")
    if user_id in SUDOERS:
        return await message.reply_text(
            "👑 **𝗤𝘂𝗲𝗿 𝗯𝗮𝗻𝗶𝗿 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲𝗹𝗲𝘃𝗮𝗱𝗼? 𝗥𝗲𝗰𝗼𝗻𝘀𝗶𝗱𝗲𝗿𝗲!**")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "⚠️ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗯𝗮𝗻𝗶𝗿 𝘂𝗺 𝗮𝗱𝗺𝗶𝗻. 𝗩𝗼𝗰𝗲̂ 𝗰𝗼𝗻𝗵𝗲𝗰𝗲 𝗮𝘀 𝗿𝗲𝗴𝗿𝗮𝘀, 𝗲 𝗲𝘂 𝘁𝗮𝗺𝗯𝗲́𝗺.**"
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "𝗔𝗻𝗼̂𝗻𝗶𝗺𝗼"
        )

    msg = (
        f"**🚫 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 𝗯𝗮𝗻𝗶𝗱𝗼:** {mention}\n"
        f"**👤 𝗕𝗮𝗻𝗶𝗱𝗼 𝗽𝗼𝗿:** {message.from_user.mention if message.from_user else '𝗔𝗻𝗼̂𝗻𝗶𝗺𝗼'}\n"
    )
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**⏳ 𝗕𝗮𝗻𝗶𝗱𝗼 𝗽𝗼𝗿:** {time_value}\n"
        if temp_reason:
            msg += f"**📄 𝗠𝗼𝘁𝗶𝘃𝗼:** {temp_reason}"
        with suppress(AttributeError):
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                replied_message = message.reply_to_message
                if replied_message:
                    message = replied_message
                await message.reply_text(msg)
            else:
                await message.reply_text("⚠️ **𝗡𝗮̃𝗼 𝗲́ 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝘂𝘀𝗮𝗿 𝗺𝗮𝗶𝘀 𝗱𝗲 𝟵𝟵.**")
        return
    if reason:
        msg += f"**📄 𝗠𝗼𝘁𝗶𝘃𝗼:** {reason}"
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)


# Unban members


@app.on_message(filters.command("unban") & ~filters.private & ~BANNED_USERS)
@admins_only("can_restrict_members")
async def unban_func(_, message: Message):
    reply = message.reply_to_message
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")

    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await message.reply_text("⚠️ **𝗡𝗮̃𝗼 𝗲́ 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗱𝗲𝘀𝗯𝗮𝗻𝗶𝗿 𝘂𝗺 𝗰𝗮𝗻𝗮𝗹.**")

    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(f"🔓 **𝗗𝗲𝘀𝗯𝗮𝗻𝗶𝗱𝗼!** {umention}")


# Promote Members


@app.on_message(
    filters.command(["promote", "fullpromote"]) & ~filters.private & ~BANNED_USERS
)
@admins_only("can_promote_members")
async def promote_func(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")

    bot = (await app.get_chat_member(message.chat.id, app.id)).privileges
    if user_id == app.id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗺𝗲 𝗽𝗿𝗼𝗺𝗼𝘃𝗲𝗿.**")
    if not bot:
        return await message.reply_text("⚠️ **𝗡𝗮̃𝗼 𝘀𝗼𝘂 𝗮𝗱𝗺𝗶𝗻 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼.**")
    if not bot.can_promote_members:
        return await message.reply_text("⚠️ **𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝘀𝘂𝗳𝗶𝗰𝗶𝗲𝗻𝘁𝗲.**")

    umention = (await app.get_users(user_id)).mention

    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=bot.can_change_info,
                can_invite_users=bot.can_invite_users,
                can_delete_messages=bot.can_delete_messages,
                can_restrict_members=bot.can_restrict_members,
                can_pin_messages=bot.can_pin_messages,
                can_promote_members=bot.can_promote_members,
                can_manage_chat=bot.can_manage_chat,
                can_manage_video_chats=bot.can_manage_video_chats,
            ),
        )
        return await message.reply_text(f"🏆 **𝗣𝗿𝗼𝗺𝗼𝘃𝗶𝗱𝗼 𝗰𝗼𝗺 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗼̃𝗲𝘀!** {umention}")

    await message.chat.promote_member(
        user_id=user_id,
        privileges=ChatPrivileges(
            can_change_info=False,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
    )
    await message.reply_text(f"🏅 **𝗣𝗿𝗼𝗺𝗼𝘃𝗶𝗱𝗼!** {umention}")


# Demote Member


@app.on_message(filters.command("purge") & ~filters.private)
@admins_only("can_delete_messages")
async def purge_func(_, message: Message):
    repliedmsg = message.reply_to_message
    await message.delete()

    if not repliedmsg:
        return await message.reply_text(
            "⚠️ **𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗶𝗻𝗶𝗰𝗶𝗮𝗿 𝗮 𝗹𝗶𝗺𝗽𝗲𝘇𝗮.**")

    cmd = message.command
    if len(cmd) > 1 and cmd[1].isdigit():
        purge_to = repliedmsg.id + int(cmd[1])
        if purge_to > message.id:
            purge_to = message.id
    else:
        purge_to = message.id

    chat_id = message.chat.id
    message_ids = []

    for message_id in range(
            repliedmsg.id,
            purge_to,
    ):
        message_ids.append(message_id)

        if len(message_ids) == 100:
            await app.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,  # Para ambos os lados
            )

            message_ids = []

    if len(message_ids) > 0:
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )


@app.on_message(filters.command("del") & ~filters.private)
@admins_only("can_delete_messages")
async def delete_func(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ **𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗲𝘅𝗰𝗹𝘂𝗶-𝗹𝗮.**")
    await message.reply_to_message.delete()
    await message.delete()


@app.on_message(filters.command("demote") & ~filters.private & ~BANNED_USERS)
@admins_only("can_promote_members")
async def demote(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")
    if user_id == app.id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗺𝗲 𝗿𝗲𝗯𝗮𝗶𝘅𝗮𝗿.**")
    if user_id in SUDOERS:
        return await message.reply_text(
            "👑 **𝗤𝘂𝗲𝗿 𝗿𝗲𝗯𝗮𝗶𝘅𝗮𝗿 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲𝗹𝗲𝘃𝗮𝗱𝗼? 𝗥𝗲𝗰𝗼𝗻𝘀𝗶𝗱𝗲𝗿𝗲!**"
        )
    try:
        member = await app.get_chat_member(message.chat.id, user_id)
        if member.status == ChatMemberStatus.ADMINISTRATOR:
            await message.chat.promote_member(
                user_id=user_id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False,
                ),
            )
            umention = (await app.get_users(user_id)).mention
            await message.reply_text(f"⬇️ **𝗥𝗲𝗯𝗮𝗶𝘅𝗮𝗱𝗼!** {umention}")
        else:
            await message.reply_text("⚠️ **𝗔 𝗽𝗲𝘀𝘀𝗼𝗮 𝗺𝗲𝗻𝗰𝗶𝗼𝗻𝗮𝗱𝗮 𝗻𝗮̃𝗼 𝗲́ 𝗮𝗱𝗺𝗶𝗻.**")
    except Exception as e:
        await message.reply_text(f"⚠️ **Erro:** {e}")


# Pin Messages


@app.on_message(filters.command(["unpinall"]) & filters.group & ~BANNED_USERS)
@admins_only("can_pin_messages")
async def pin(_, message: Message):
    if message.command[0] == "unpinall":
        return await message.reply_text(
            "⚠️ **𝗧𝗲𝗺 𝗰𝗲𝗿𝘁𝗲𝘇𝗮 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗱𝗲𝘀𝗳𝗶𝘅𝗮𝗿 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀?**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✔️ 𝗦𝗶𝗺", callback_data="unpin_yes"),
                        InlineKeyboardButton(text="❌ 𝗡𝗮̃𝗼", callback_data="unpin_no"),
                    ],
                ]
            ),
        )


@app.on_callback_query(filters.regex(r"unpin_(yes|no)"))
async def callback_query_handler(_, query: CallbackQuery):
    if query.data == "unpin_yes":
        await app.unpin_all_chat_messages(query.message.chat.id)
        return await query.message.edit_text(
            "📌 **𝗧𝗼𝗱𝗮𝘀 𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗳𝗶𝘅𝗮𝗱𝗮𝘀 𝗳𝗼𝗿𝗮𝗺 𝗱𝗲𝘀𝗳𝗶𝘅𝗮𝗱𝗮𝘀.**")
    elif query.data == "unpin_no":
        return await query.message.edit_text(
            "❌ **𝗢 𝗱𝗲𝘀𝗳𝗶𝘅𝗮𝗿 𝗱𝗲 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗳𝗼𝗶 𝗰𝗮𝗻𝗰𝗲𝗹𝗮𝗱𝗼.**"
        )


@app.on_message(filters.command(["pin", "unpin"]) & ~filters.private & ~BANNED_USERS)
@admins_only("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "⚠️ **𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗳𝗶𝘅𝗮𝗿/𝗱𝗲𝘀𝗳𝗶𝘅𝗮𝗿.**")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.reply_text(
            f"📌 **𝗠𝗲𝗻𝘀𝗮𝗴𝗲𝗺 [𝗱𝗲𝘀𝗳𝗶𝘅𝗮𝗱𝗮]({r.link}).**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await message.reply(
        f"📌 **𝗠𝗲𝗻𝘀𝗮𝗴𝗲𝗺 [𝗳𝗶𝘅𝗮𝗱𝗮]({r.link}).**",
        disable_web_page_preview=True,
    )
    msg = "🔔 **𝗖𝗼𝗻𝗳𝗶𝗿𝗮 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗳𝗶𝘅𝗮𝗱𝗮:** ~ " + f"[𝗖𝗼𝗻𝗳𝗶𝗿𝗮, {r.link}]"
    filter_ = dict(type="text", data=msg)
    await save_filter(message.chat.id, "~pinned", filter_)


# Mute members


@app.on_message(filters.command(["mute", "tmute"]) & ~filters.private & ~BANNED_USERS)
@admins_only("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")
    if user_id == app.id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗺𝗲 𝘀𝗶𝗹𝗲𝗻𝗰𝗶𝗮𝗿.**")
    if user_id in SUDOERS:
        return await message.reply_text(
            "👑 **𝗤𝘂𝗲𝗿 𝘀𝗶𝗹𝗲𝗻𝗰𝗶𝗮𝗿 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲𝗹𝗲𝘃𝗮𝗱𝗼? 𝗥𝗲𝗰𝗼𝗻𝘀𝗶𝗱𝗲𝗿𝗲!**")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "⚠️ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝘀𝗶𝗹𝗲𝗻𝗰𝗶𝗮𝗿 𝘂𝗺 𝗮𝗱𝗺𝗶𝗻. 𝗩𝗼𝗰𝗲̂ 𝗰𝗼𝗻𝗵𝗲𝗰𝗲 𝗮𝘀 𝗿𝗲𝗴𝗿𝗮𝘀, 𝗲 𝗲𝘂 𝘁𝗮𝗺𝗯𝗲́𝗺.**"
        )
    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"🔊 𝗔𝘁𝗶𝘃𝗮𝗿 𝗮𝘂́𝗱𝗶𝗼": f"unmute_{user_id}"})
    msg = (
        f"🔇 **𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 𝘀𝗶𝗹𝗲𝗻𝗰𝗶𝗮𝗱𝗼:** {mention}\n"
        f"👤 **𝗦𝗶𝗹𝗲𝗻𝗰𝗶𝗮𝗱𝗼 𝗽𝗼𝗿:** {message.from_user.mention if message.from_user else '𝗔𝗻𝗼̂𝗻𝗶𝗺𝗼'}\n"
    )
    if message.command[0] == "tmute":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_mute = await time_converter(message, time_value)
        msg += f"⏳ **𝗦𝗶𝗹𝗲𝗻𝗰𝗶𝗮𝗱𝗼 𝗽𝗼𝗿:** {time_value}\n"
        if temp_reason:
            msg += f"📄 **𝗠𝗼𝘁𝗶𝘃𝗼:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(),
                    until_date=temp_mute,
                )
                replied_message = message.reply_to_message
                if replied_message:
                    message = replied_message
                await message.reply_text(msg, reply_markup=keyboard)
            else:
                await message.reply_text("⚠️ **𝗡𝗮̃𝗼 𝗲́ 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝘂𝘀𝗮𝗿 𝗺𝗮𝗶𝘀 𝗱𝗲 𝟵𝟵.**")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"📄 **𝗠𝗼𝘁𝗶𝘃𝗼:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg, reply_markup=keyboard)


@app.on_message(filters.command("unmute") & ~filters.private & ~BANNED_USERS)
@admins_only("can_restrict_members")
async def unmute(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")
    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(f"🔊 **𝗔𝘂́𝗱𝗶𝗼 𝗿𝗲𝘀𝘁𝗮𝘂𝗿𝗮𝗱𝗼!** {umention}")


@app.on_message(filters.command(["warn", "swarn"]) & ~filters.private & ~BANNED_USERS)
@admins_only("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")
    if user_id == app.id:
        return await message.reply_text(
            "❌ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗺𝗲 𝗮𝘃𝗶𝘀𝗮𝗿, 𝗺𝗮𝘀 𝗽𝗼𝘀𝘀𝗼 𝘀𝗮𝗶𝗿 𝘀𝗲 𝗾𝘂𝗶𝘀𝗲𝗿.**")
    if user_id in SUDOERS:
        return await message.reply_text(
            "👑 **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗮𝘃𝗶𝘀𝗮𝗿 𝘂𝗺 𝗴𝗲𝗿𝗲𝗻𝘁𝗲, 𝗲𝗹𝗲 𝗺𝗲 𝗴𝗲𝗿𝗲𝗻𝗰𝗶𝗮!**")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "⚠️ **𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗮𝘃𝗶𝘀𝗮𝗿 𝘂𝗺 𝗮𝗱𝗺𝗶𝗻, 𝗿𝗲𝗴𝗿𝗮𝘀 𝘀𝗮̃𝗼 𝗿𝗲𝗴𝗿𝗮𝘀.**")
    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    mention = user.mention
    keyboard = ikb({"🚨 **Remover Aviso** 🚨": f"unwarn_{user_id}"})
    warns = warns["warns"] if warns else 0
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)
    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"🔴 **𝗡𝗮𝗱𝗮 𝗱𝗲 𝗮𝘃𝗶𝘀𝗼𝘀 𝗲𝘅𝗰𝗲𝗱𝗶𝗱𝗼𝘀 𝗽𝗮𝗿𝗮 {mention}! 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 𝗯𝗮𝗻𝗶𝗱𝗼!**")
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
**⚠️ Usuário Avisado:** {mention}
**🔹 Avisado Por:** {message.from_user.mention if message.from_user else '𝗔𝗻𝗼̂𝗻𝗶𝗺𝗼'}
**📄 Motivo:** {reason or 'Nenhum motivo fornecido'}
**⚠️ Avisos:** {warns + 1}/3"""
        replied_message = message.reply_to_message
        if replied_message:
            message = replied_message
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


@app.on_callback_query(filters.regex("unwarn_") & ~BANNED_USERS)
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "❌ **𝗩𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝘁𝗲𝗺 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝘀𝘂𝗳𝗶𝗰𝗶𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 𝗿𝗲𝗮𝗹𝗶𝘇𝗮𝗿 𝗲𝘀𝘀𝗮 𝗮𝗰̧𝗮̃𝗼.**\n"
            + f"**𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗻𝗲𝗰𝗲𝘀𝘀𝗮́𝗿𝗶𝗮:** {permission}",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    warns = warns["warns"] if warns else 0
    if not warns:
        return await cq.answer("⚠️ **O usuário não tem avisos.**")
    warn = {"warns": warns - 1}
    await add_warn(chat_id, await int_to_alpha(user_id), warn)
    text = f"~~{cq.message.text.markdown}~~\n\n__Aviso removido por {from_user.mention}__"
    await cq.message.edit(text)


@app.on_message(filters.command("rmwarns") & ~filters.private & ~BANNED_USERS)
@admins_only("can_restrict_members")
async def remove_warnings(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")
    mention = (await app.get_users(user_id)).mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    warns = warns["warns"] if warns else 0
    if warns == 0:
        await message.reply_text(f"✅ **{mention} não possui avisos.**")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"🗑️ **Avisos de {mention} foram removidos.**")


@app.on_message(filters.command("warns") & ~filters.private & ~BANNED_USERS)
@capture_err
async def check_warns(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("❌ **𝗡𝗮̃𝗼 𝗰𝗼𝗻𝘀𝗲𝗴𝘂𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**")
    warns = await get_warn(message.chat.id, await int_to_alpha(user_id))
    mention = (await app.get_users(user_id)).mention
    warns = warns["warns"] if warns else 0
    if warns == 0:
        return await message.reply_text(f"✅ **{mention} não possui avisos.**")
    return await message.reply_text(f"⚠️ **{mention} possui {warns}/3 avisos.**")


@app.on_message(filters.command("link") & ~BANNED_USERS)
@admins_only("can_invite_users")
async def invite(_, message):
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        link = (await app.get_chat(message.chat.id)).invite_link
        if not link:
            link = await app.export_chat_invite_link(message.chat.id)
        text = f"🔗 **Aqui está o link de convite do grupo:**\n\n{link}"
        if message.reply_to_message:
            await message.reply_to_message.reply_text(
                text, disable_web_page_preview=True
            )
        else:
            await message.reply_text(text, disable_web_page_preview=True)
