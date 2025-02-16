import asyncio

from Cecilia import app
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

SPAM_CHATS = []


async def is_admin(chat_id, user_id):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    if user_id in admin_ids:
        return True
    return False


@app.on_message(
    filters.command(["all", "allmention", "mentionall", "tagall"], prefixes=["/", "@"])
)
async def tag_all_users(_, message):
    admin = await is_admin(message.chat.id, message.from_user.id)
    if not admin:
        return

    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "𝗢 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗼 𝗱𝗲 𝗺𝗮𝗿𝗰𝗮𝗰̧𝗮̃𝗼 𝗷𝗮́ 𝗲𝘀𝘁𝗮́ 𝗲𝗺 𝗮𝗻𝗱𝗮𝗺𝗲𝗻𝘁𝗼 🛑! 𝗦𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗶𝗻𝘁𝗲𝗿𝗿𝗼𝗺𝗽𝗲𝗿, 𝘂𝘀𝗲 /cancel."
        )
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "🔹 **𝙋𝙧𝙚𝙘𝙞𝙨𝙤 𝙦𝙪𝙚 𝙫𝙤𝙘𝙚̂ 𝙚𝙣𝙫𝙞𝙚 𝙪𝙢𝙖 𝙢𝙚𝙣𝙨𝙖𝙜𝙚𝙢 𝙥𝙖𝙧𝙖 𝙢𝙖𝙧𝙘𝙖𝙧 𝙩𝙤𝙙𝙤𝙨, 𝙘𝙤𝙢𝙤 »** `@all Olá pessoal!`"
        )
        return
    if replied:
        usernum = 0
        usertxt = ""
        try:
            SPAM_CHATS.append(message.chat.id)
            async for m in app.get_chat_members(message.chat.id):
                if message.chat.id not in SPAM_CHATS:
                    break
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(1)
                    usernum = 0
                    usertxt = ""

            if usernum != 0:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        try:
            usernum = 0
            usertxt = ""
            text = message.text.split(None, 1)[1]
            SPAM_CHATS.append(message.chat.id)
            async for m in app.get_chat_members(message.chat.id):
                if message.chat.id not in SPAM_CHATS:
                    break
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await app.send_message(
                        message.chat.id,
                        f"{text}\n{usertxt}",
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(2)
                    usernum = 0
                    usertxt = ""
            if usernum != 0:
                await app.send_message(
                    message.chat.id,
                    f"{text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass


async def tag_all_admins(_, message):
    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "𝗢 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗼 𝗱𝗲 𝗺𝗮𝗿𝗰𝗮𝗰̧𝗮̃𝗼 𝗷𝗮́ 𝗲𝘀𝘁𝗮́ 𝗲𝗺 𝗮𝗻𝗱𝗮𝗺𝗲𝗻𝘁𝗼 🛑! 𝗦𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗶𝗻𝘁𝗲𝗿𝗿𝗼𝗺𝗽𝗲𝗿, 𝘂𝘀𝗲 /cancel."
        )
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "🔹 **𝙋𝙧𝙚𝙘𝙞𝙨𝙤 𝙦𝙪𝙚 𝙫𝙤𝙘𝙚̂ 𝙚𝙣𝙫𝙞𝙚 𝙪𝙢𝙖 𝙢𝙚𝙣𝙨𝙖𝙜𝙚𝙢 𝙥𝙖𝙧𝙖 𝙢𝙖𝙧𝙘𝙖𝙧 𝙩𝙤𝙙𝙤𝙨 𝙤𝙨 𝙖𝙙𝙢𝙞𝙣𝙨, 𝙘𝙤𝙢𝙤 »** `@admins Olá equipe!`"
        )
        return
    if replied:
        usernum = 0
        usertxt = ""
        try:
            SPAM_CHATS.append(message.chat.id)
            async for m in app.get_chat_members(
                    message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if message.chat.id not in SPAM_CHATS:
                    break
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(1)
                    usernum = 0
                    usertxt = ""
            if usernum != 0:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        usernum = 0
        usertxt = ""
        try:
            text = message.text.split(None, 1)[1]
            SPAM_CHATS.append(message.chat.id)
            async for m in app.get_chat_members(
                    message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if message.chat.id not in SPAM_CHATS:
                    break
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await app.send_message(
                        message.chat.id,
                        f"{text}\n{usertxt}",
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(2)
                    usernum = 0
                    usertxt = ""
            if usernum != 0:
                await app.send_message(
                    message.chat.id,
                    f"{text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass


@app.on_message(
    filters.command(
        [
            "stopmention",
            "cancel",
            "cancelmention",
            "offmention",
            "mentionoff",
            "cancelall",
        ],
        prefixes=["/", "@"],
    )
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    admin = await is_admin(chat_id, message.from_user.id)
    if not admin:
        return
    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass
        return await message.reply_text(
            "🛑 **𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗼 𝗱𝗲 𝗺𝗮𝗿𝗰𝗮𝗰̧𝗮̃𝗼 𝗶𝗻𝘁𝗲𝗿𝗿𝗼𝗺𝗽𝗶𝗱𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼!**")

    else:
        await message.reply_text("⚠️ **𝗡𝗲𝗻𝗵𝘂𝗺 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗼 𝗲𝘀𝘁𝗮́ 𝗲𝗺 𝗮𝗻𝗱𝗮𝗺𝗲𝗻𝘁𝗼!**")
        return


__MODULE__ = "🔹𝗠𝗮𝗿𝗰𝗮𝗿"
__HELP__ = """

@all ou /all | /tagall ou @tagall | /mentionall ou @mentionall [texto] ou [responder a qualquer mensagem] para marcar todos os usuários no grupo pelo bot 🤖

/admins | @admins | /report [texto] ou [responder a qualquer mensagem] para marcar todos os administradores do grupo 👮

/cancel ou @cancel | /offmention ou @offmention | /mentionoff ou @mentionoff | /cancelall ou @cancelall - para interromper qualquer processo de marcação em andamento ❌

**__A𝘁𝗲𝗻𝗰̧𝗮̃𝗼__** Este comando pode ser usado apenas pelos administradores do chat e certifique-se de que o bot e o assistente sejam administradores no seu grupo 🔒
"""
