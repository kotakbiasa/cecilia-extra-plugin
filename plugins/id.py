from WinxMusic import app
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command("id"))
async def get_id(_, message: Message):
    try:
        if not message.reply_to_message and message.chat:
            await message.reply(
                f"👤 𝗨𝘀𝘂𝗮𝗿𝗶𝗼 <b>{message.from_user.first_name}'𝘀</b> 𝗜𝗗 𝗲́ <code>{message.from_user.id}</code>.\n💬 𝗢 𝗜𝗗 𝗱𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁 𝗲́: <code>{message.chat.id}</code>."
            )
        elif not message.reply_to_message.sticker or message.reply_to_message is None:
            if message.reply_to_message.forward_from_chat:
                await message.reply(
                    f"📥 𝗢 𝗰𝗮𝗻𝗮𝗹 𝗳𝗼𝗿𝘄𝗮𝗿𝗱𝗮𝗱𝗼, {message.reply_to_message.forward_from_chat.title}, 𝗽𝗼𝘀𝘀𝘂𝗶 𝗼 𝗜𝗗 <code>{message.reply_to_message.forward_from_chat.id}</code>"
                )

            elif message.reply_to_message.forward_from:
                await message.reply(
                    f"👤 𝗢 𝘂𝘀𝘂𝗮𝗿𝗶𝗼 𝗳𝗼𝗿𝘄𝗮𝗿𝗱𝗮𝗱𝗼, {message.reply_to_message.forward_from.first_name}, 𝗽𝗼𝘀𝘀𝘂𝗶 𝗼 𝗜𝗗 <code>{message.reply_to_message.forward_from.id}</code>."
                )

            elif message.reply_to_message.forward_sender_name:
                await message.reply(
                    "❗ 𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲, 𝗻𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗿𝗲𝗰𝘂𝗽𝗲𝗿𝗮𝗿 𝗼 𝗜𝗗 𝗱𝗼 𝘂𝘀𝘂𝗮𝗿𝗶𝗼."
                )
            else:
                await message.reply(
                    f"👤 𝗨𝘀𝘂𝗮𝗿𝗶𝗼 {message.reply_to_message.from_user.first_name} 𝗽𝗼𝘀𝘀𝘂𝗶 𝗼 𝗜𝗗 <code>{message.reply_to_message.from_user.id}</code>."
                )
        elif message.reply_to_message.sticker:
            if message.reply_to_message.forward_from_chat:
                await message.reply(
                    f"📥 𝗢 𝗰𝗮𝗻𝗮𝗹 𝗳𝗼𝗿𝘄𝗮𝗿𝗱𝗮𝗱𝗼, {message.reply_to_message.forward_from_chat.title}, 𝗽𝗼𝘀𝘀𝘂𝗶 𝗼 𝗜𝗗 <code>{message.reply_to_message.forward_from_chat.id}</code> \n🖼️ 𝗘 𝗼 𝗜𝗗 𝗱𝗼 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗲́ <code>{message.reply_to_message.sticker.file_id}</code>"
                )

            elif message.reply_to_message.forward_from:
                await message.reply(
                    f"👤 𝗢 𝘂𝘀𝘂𝗮𝗿𝗶𝗼 𝗳𝗼𝗿𝘄𝗮𝗿𝗱𝗮𝗱𝗼, {message.reply_to_message.forward_from.first_name}, 𝗽𝗼𝘀𝘀𝘂𝗶 𝗼 𝗜𝗗 <code>{message.reply_to_message.forward_from.id}</code> \n🖼️ 𝗘 𝗼 𝗜𝗗 𝗱𝗼 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗲́ <code>{message.reply_to_message.sticker.file_id}</code>."
                )

            elif message.reply_to_message.forward_sender_name:
                await message.reply(
                    "❗ 𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲, 𝗻𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗿𝗲𝗰𝘂𝗽𝗲𝗿𝗮𝗿 𝗼 𝗜𝗗 𝗱𝗼 𝘂𝘀𝘂𝗮𝗿𝗶𝗼."
                )

            else:
                await message.reply(
                    f"👤 𝗨𝘀𝘂𝗮𝗿𝗶𝗼 {message.reply_to_message.from_user.first_name} 𝗽𝗼𝘀𝘀𝘂𝗶 𝗼 𝗜𝗗 <code>{message.reply_to_message.from_user.id}</code>\n🖼️ 𝗘 𝗼 𝗜𝗗 𝗱𝗼 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗲́ <code>{message.reply_to_message.sticker.file_id}</code>."
                )
        else:
            await message.reply(
                f"👤 𝗨𝘀𝘂𝗮𝗿𝗶𝗼 {message.reply_to_message.from_user.first_name} 𝗽𝗼𝘀𝘀𝘂𝗶 𝗼 𝗜𝗗 <code>{message.reply_to_message.from_user.id}</code>."
            )
    except Exception as r:
        await message.reply(f"⚠️ 𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝗼 𝗜𝗗. {r}")


__MODULE__ = "🆔𝗜𝗗"
__HELP__ = """
**📘 𝗥𝗲𝗰𝘂𝗽𝗲𝗿𝗮𝗱𝗼𝗿 𝗱𝗲 𝗜𝗗:**

• `/id`: 𝗥𝗲𝗰𝘂𝗽𝗲𝗿𝗲 𝗼𝘀 𝗜𝗗𝘀 𝗱𝗲 𝘂𝘀𝘂𝗮𝗿𝗶𝗼𝘀 𝗲 𝗱𝗲 𝗰𝗵𝗮𝘁𝘀.
"""
