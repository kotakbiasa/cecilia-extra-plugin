from typing import Dict, Union

from WinxMusic import app
from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message

mongo = MongoCli(MONGO_DB_URI).Rankings

impdb = mongo.pretender


async def usr_data(chat_id: int, user_id: int) -> bool:
    user = await impdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return bool(user)


async def get_userdata(chat_id: int, user_id: int) -> Union[Dict[str, str], None]:
    user = await impdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return user


async def add_userdata(
        chat_id: int, user_id: int, username: str, first_name: str, last_name: str
):
    await impdb.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        },
        upsert=True,
    )


async def check_pretender(chat_id: int) -> bool:
    chat = await impdb.find_one({"chat_id_toggle": chat_id})
    return bool(chat)


async def impo_on(chat_id: int) -> None:
    await impdb.insert_one({"chat_id_toggle": chat_id})


async def impo_off(chat_id: int) -> None:
    await impdb.delete_one({"chat_id_toggle": chat_id})


@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    chat_id = message.chat.id
    if message.sender_chat or not await check_pretender(chat_id):
        return
    user_id = message.from_user.id
    user_data = await get_userdata(chat_id, user_id)
    if not user_data:
        await add_userdata(
            chat_id,
            user_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        return

    usernamebefore = user_data.get("username", "")
    first_name = user_data.get("first_name", "")
    lastname_before = user_data.get("last_name", "")

    msg = f"[{message.from_user.id}](tg://user?id={message.from_user.id})\n"

    changes = []

    if (
            first_name != message.from_user.first_name
            and lastname_before != message.from_user.last_name
    ):
        changes.append(
            f"📝 𝗺𝘂𝗱𝗼𝘂 𝗼 𝗻𝗼𝗺𝗲 𝗱𝗲 {first_name} {lastname_before} 𝗽𝗮𝗿𝗮 {message.from_user.first_name} {message.from_user.last_name}\n"
        )
    elif first_name != message.from_user.first_name:
        changes.append(
            f"📝 𝗺𝘂𝗱𝗼𝘂 𝗼 𝗽𝗿𝗶𝗺𝗲𝗶𝗿𝗼 𝗻𝗼𝗺𝗲 𝗱𝗲 {first_name} 𝗽𝗮𝗿𝗮 {message.from_user.first_name}\n"
        )
    elif lastname_before != message.from_user.last_name:
        changes.append(
            f"📝 𝗺𝘂𝗱𝗼𝘂 𝗼 𝘀𝗼𝗯𝗿𝗲𝗻𝗼𝗺𝗲 𝗱𝗲 {lastname_before} 𝗽𝗮𝗿𝗮 {message.from_user.last_name}\n"
        )

    if usernamebefore != message.from_user.username:
        changes.append(
            f"👤 𝗺𝘂𝗱𝗼𝘂 𝗼 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗱𝗲 @{usernamebefore} 𝗽𝗮𝗿𝗮 @{message.from_user.username}\n"
        )

    if changes:
        msg += "".join(changes)
        await message.reply_text(msg)

    await add_userdata(
        chat_id,
        user_id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )


@app.on_message(
    filters.group & filters.command("pretender") & ~filters.bot & ~filters.via_bot
)
async def set_mataa(_, message: Message):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    if message.from_user.id not in admin_ids:
        return
    if len(message.command) == 1:
        return await message.reply("⚠️ **𝗨𝘀𝗼 𝗱𝗲 𝗽𝗿𝗲𝘁𝗲𝗻𝗱𝗲𝗿 𝗱𝗲𝘁𝗲𝗰𝘁𝗮𝗱𝗼:\n/pretender on|off**")
    chat_id = message.chat.id
    if message.command[1] == "on":
        cekset = await check_pretender(chat_id)
        if cekset:
            await message.reply(
                f"✅ 𝗽𝗿𝗲𝘁𝗲𝗻𝗱𝗲𝗿 𝗷𝗮́ 𝗲𝘀𝘁𝗮́ 𝗮𝘁𝗶𝘃𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 **{message.chat.title}**"
            )
        else:
            await impo_on(chat_id)
            await message.reply(
                f"🎉 𝗽𝗿𝗲𝘁𝗲𝗻𝗱𝗲𝗿 𝗮𝘁𝗶𝘃𝗮𝗱𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼 𝗽𝗮𝗿𝗮 **{message.chat.title}**"
            )
    elif message.command[1] == "off":
        cekset = await check_pretender(chat_id)
        if not cekset:
            await message.reply(
                f"ℹ️ 𝗽𝗿𝗲𝘁𝗲𝗻𝗱𝗲𝗿 𝗷𝗮́ 𝗲𝘀𝘁𝗮́ 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 **{message.chat.title}**"
            )
        else:
            await impo_off(chat_id)
            await message.reply(
                f"🎉 𝗽𝗿𝗲𝘁𝗲𝗻𝗱𝗲𝗿 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗱𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼 𝗽𝗮𝗿𝗮 **{message.chat.title}**"
            )
    else:
        await message.reply("⚠️ **𝗨𝘀𝗼 𝗱𝗲 𝗽𝗿𝗲𝘁𝗲𝗻𝗱𝗲𝗿 𝗱𝗲𝘁𝗲𝗰𝘁𝗮𝗱𝗼:\n/pretender on|off**")


__MODULE__ = "🕵️𝗣𝗿𝗲𝘁𝗲𝗻𝗱𝗲𝗿"
__HELP__ = """
ℹ️ /pretender - [on / off] - 𝗽𝗮𝗿𝗮 𝗮𝘁𝗶𝘃𝗮𝗿 𝗼𝘂 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗿 𝗽𝗿𝗲𝘁𝗲𝗻𝗱𝗲𝗿 𝗽𝗮𝗿𝗮 𝗼 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁. 𝗦𝗲 𝗮𝗹𝗴𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗺𝘂𝗱𝗮𝗿 𝘀𝗲𝘂 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼, 𝗻𝗼𝗺𝗲, 𝗯𝗶𝗼, 𝗼 𝗯𝗼𝘁 𝗲𝗻𝘃𝗶𝗮𝗿𝗮́ 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗻𝗼 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁
"""
