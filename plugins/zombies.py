import asyncio

from WinxMusic import app
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from utils.permissions import adminsOnly

chat_queue = []

stop_process = False


@app.on_message(filters.command(["zombies"]))
@adminsOnly("can_restrict_members")
async def remove(_, message: Message):
    global stop_process
    try:
        try:
            sender = await app.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except BaseException:
            has_permissions = message.sender_chat
        if has_permissions:
            bot = await app.get_chat_member(message.chat.id, "self")
            if bot.status == ChatMemberStatus.MEMBER:
                await message.reply(
                    "🚨 | **𝗘𝘂 𝗽𝗿𝗲𝗰𝗶𝘀𝗼 𝗱𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗼̃𝗲𝘀 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 𝗽𝗮𝗿𝗮 𝗿𝗲𝗺𝗼𝘃𝗲𝗿 𝗰𝗼𝗻𝘁𝗮𝘀 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗮𝘀.**"
                )
            else:
                if len(chat_queue) > 30:
                    await message.reply(
                        "⚠️ | **𝗝𝗮́ 𝗲𝘀𝘁𝗼𝘂 𝗻𝗼 𝗹𝗶𝗺𝗶𝘁𝗲 𝗺𝗮́𝘅𝗶𝗺𝗼 𝗱𝗲 𝟯𝟬 𝗰𝗵𝗮𝘁𝘀 𝗻𝗼 𝗺𝗼𝗺𝗲𝗻𝘁𝗼. 𝗧𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗲𝗺 𝗯𝗿𝗲𝘃𝗲!**"
                    )
                else:
                    if message.chat.id in chat_queue:
                        await message.reply(
                            "🔄 | **𝗝𝗮́ 𝗲𝘅𝗶𝘀𝘁𝗲 𝘂𝗺 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗼 𝗲𝗺 𝗮𝗻𝗱𝗮𝗺𝗲𝗻𝘁𝗼 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁. 𝗨𝘀𝗲 `/stop` 𝗽𝗮𝗿𝗮 𝗶𝗻𝗶𝗰𝗶𝗮𝗿 𝘂𝗺 𝗻𝗼𝘃𝗼.**"
                        )
                    else:
                        chat_queue.append(message.chat.id)
                        deletedList = []
                        async for member in app.get_chat_members(message.chat.id):
                            if member.user.is_deleted:
                                deletedList.append(member.user)
                        lenDeletedList = len(deletedList)
                        if lenDeletedList == 0:
                            await message.reply(
                                "✔️ | **𝗡𝗮̃𝗼 𝗵𝗮́ 𝗰𝗼𝗻𝘁𝗮𝘀 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗮𝘀 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁.**")
                            chat_queue.remove(message.chat.id)
                        else:
                            k = 0
                            processTime = lenDeletedList * 1
                            temp = await app.send_message(
                                message.chat.id,
                                f"🧭 | **𝗧𝗼𝘁𝗮𝗹 𝗱𝗲 {lenDeletedList} 𝗰𝗼𝗻𝘁𝗮𝘀 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗮𝘀 𝗱𝗲𝘁𝗲𝗰𝘁𝗮𝗱𝗮𝘀.**\n⏳ | **𝗧𝗲𝗺𝗽𝗼 𝗲𝘀𝘁𝗶𝗺𝗮𝗱𝗼:** {processTime} 𝘀𝗲𝗴𝘂𝗻𝗱𝗼𝘀.",
                            )
                            if stop_process:
                                stop_process = False
                            while len(deletedList) > 0 and not stop_process:
                                deletedAccount = deletedList.pop(0)
                                try:
                                    await app.ban_chat_member(
                                        message.chat.id, deletedAccount.id
                                    )
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                except Exception:
                                    pass
                                k += 1
                            if k == lenDeletedList:
                                await message.reply(
                                    f"✅ | **𝗥𝗲𝗺𝗼𝘃𝗶𝗱𝗮𝘀 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗰𝗼𝗻𝘁𝗮𝘀 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗮𝘀 𝗱𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼.**"
                                )
                                await temp.delete()
                            else:
                                await message.reply(
                                    f"✅ | **𝗥𝗲𝗺𝗼𝘃𝗶𝗱𝗮𝘀 {k} 𝗰𝗼𝗻𝘁𝗮𝘀 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗮𝘀 𝗱𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁.**"
                                )
                                await temp.delete()
                            chat_queue.remove(message.chat.id)
        else:
            await message.reply(
                "👮🏻 | **𝗔𝗽𝗲𝗻𝗮𝘀 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀 𝗽𝗼𝗱𝗲𝗺 𝗲𝘅𝗲𝗰𝘂𝘁𝗮𝗿 𝗲𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼.**"
            )
    except FloodWait as e:
        await asyncio.sleep(e.value)


__MODULE__ = "🧟‍♂️ 𝗭𝗼𝗺𝗯𝗶𝗲𝘀"
__HELP__ = """
**🧹 𝗥𝗲𝗺𝗼𝗰̧𝗮̃𝗼 𝗱𝗲 𝗖𝗼𝗻𝘁𝗮𝘀 𝗗𝗲𝗹𝗲𝘁𝗮𝗱𝗮𝘀**

• /zombies - **𝗥𝗲𝗺𝗼𝘃𝗲 𝗰𝗼𝗻𝘁𝗮𝘀 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗮𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼.**

**𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀:**
- 𝗠𝗼́𝗱𝘂𝗹𝗼: 𝗥𝗲𝗺𝗼𝘃𝗲𝗿 𝗖𝗼𝗻𝘁𝗮𝘀 𝗗𝗲𝗹𝗲𝘁𝗮𝗱𝗮𝘀
- 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗻𝗲𝗰𝗲𝘀𝘀𝗮́𝗿𝗶𝗮: 𝗣𝗼𝗱𝗲 𝗿𝗲𝘀𝘁𝗿𝗶𝗻𝗴𝗶𝗿 𝗺𝗲𝗺𝗯𝗿𝗼𝘀

**𝗡𝗼𝘁𝗮:**
- 𝗨𝘁𝗶𝗹𝗶𝘇𝗲 𝗱𝗶𝗿𝗲𝘁𝗮𝗺𝗲𝗻𝘁𝗲 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝗺𝗲𝗹𝗵𝗼𝗿𝗲𝘀 𝗿𝗲𝘀𝘂𝗹𝘁𝗮𝗱𝗼𝘀. 𝗔𝗽𝗲𝗻𝗮𝘀 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀 𝗽𝗼𝗱𝗲𝗺 𝗲𝘅𝗲𝗰𝘂𝘁𝗮𝗿 𝗲𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼.
"""
