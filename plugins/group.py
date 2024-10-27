from WinxMusic import app
from pyrogram import enums, filters
from pyrogram.types import Message

from utils.permissions import admins_only


@app.on_message(filters.command("removephoto"))
@admins_only("can_change_info")
async def delete_chat_photo(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("**𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...** 🕒")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("**𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝗮𝗽𝗲𝗻𝗮𝘀 𝗲𝗺 𝗴𝗿𝘂𝗽𝗼𝘀!**")
    try:
        if admin_check.privileges.can_change_info:
            await app.delete_chat_photo(chat_id)
            await msg.edit(
                "**𝗙𝗼𝘁𝗼 𝗱𝗼 𝗽𝗿𝗼𝗳𝗶𝗹𝗲 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗿𝗲𝗺𝗼𝘃𝗶𝗱𝗮!**\n𝗣𝗼𝗿 {}".format(
                    message.from_user.mention
                )
            )
    except BaseException:
        await msg.edit(
            "**𝗢 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗱𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝗿𝗲𝗺𝗼𝘃𝗲𝗿 𝗮 𝗳𝗼𝘁𝗼!**"
        )


@app.on_message(filters.command("setphoto"))
@admins_only("can_change_info")
async def set_chat_photo(_, message: Message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("**𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...** 🖼️")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("**𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝗮𝗽𝗲𝗻𝗮𝘀 𝗲𝗺 𝗴𝗿𝘂𝗽𝗼𝘀!**")
    elif not reply:
        await msg.edit("**𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗼𝘂 𝘂𝗺 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗱𝗲 𝗶𝗺𝗮𝗴𝗲𝗺.**")
    elif reply:
        try:
            if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text(
                    "**𝗡𝗼𝘃𝗮 𝗳𝗼𝘁𝗼 𝗱𝗼 𝗽𝗿𝗼𝗳𝗶𝗹𝗲 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗮𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗱𝗮!**\n𝗣𝗼𝗿 {}".format(
                        message.from_user.mention
                    )
                )
            else:
                await msg.edit("**𝗔𝗹𝗴𝗼 𝗲𝗿𝗿𝗮𝗱𝗼 𝗼𝗰𝗼𝗿𝗿𝗲𝘂. 𝗧𝗲𝗻𝘁𝗲 𝗼𝘂𝘁𝗿𝗮 𝗶𝗺𝗮𝗴𝗲𝗺!**")
        except BaseException:
            await msg.edit(
                "**𝗢 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗱𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗮 𝗳𝗼𝘁𝗼!**"
            )


@app.on_message(filters.command("settitle"))
@admins_only("can_change_info")
async def set_group_title(_, message: Message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("**𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...** 📝")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("**𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝗮𝗽𝗲𝗻𝗮𝘀 𝗲𝗺 𝗴𝗿𝘂𝗽𝗼𝘀!**")
    elif reply:
        try:
            title = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(
                    "**𝗡𝗼𝘃𝗼 𝗻𝗼𝗺𝗲 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗮𝗹𝘁𝗲𝗿𝗮𝗱𝗼!**\n𝗣𝗼𝗿 {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "**𝗢 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗱𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗼 𝗻𝗼𝗺𝗲!**"
            )
    elif len(message.command) > 1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(
                    "**𝗡𝗼𝘃𝗼 𝗻𝗼𝗺𝗲 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗮𝗹𝘁𝗲𝗿𝗮𝗱𝗼!**\n𝗣𝗼𝗿 {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "**𝗢 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗱𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗼 𝗻𝗼𝗺𝗲!**"
            )
    else:
        await msg.edit(
            "**𝗩𝗼𝗰𝗲̂ 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗿 𝗮 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗼𝘂 𝗳𝗼𝗿𝗻𝗲𝗰𝗲𝗿 𝘂𝗺 𝗻𝗼𝘃𝗼 𝗻𝗼𝗺𝗲 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗼 𝗻𝗼𝗺𝗲 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼!**"
        )


@app.on_message(filters.command(["setdiscription", "setdesc"]))
@admins_only("can_change_info")
async def set_group_description(_, message: Message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("**𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...** 📋")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("**𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝗮𝗽𝗲𝗻𝗮𝘀 𝗲𝗺 𝗴𝗿𝘂𝗽𝗼𝘀!**")
    elif reply:
        try:
            discription = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(
                    "**𝗡𝗼𝘃𝗮 𝗱𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗮𝗹𝘁𝗲𝗿𝗮𝗱𝗮!**\n𝗣𝗼𝗿 {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "**𝗢 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗱𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗮 𝗱𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼!**"
            )
    elif len(message.command) > 1:
        try:
            discription = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(
                    "**𝗡𝗼𝘃𝗮 𝗱𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗮𝗹𝘁𝗲𝗿𝗮𝗱𝗮!**\n𝗣𝗼𝗿 {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "**𝗢 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗱𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗮 𝗱𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼!**"
            )
    else:
        await msg.edit(
            "**𝗩𝗼𝗰𝗲̂ 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗿 𝗮 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗼𝘂 𝗳𝗼𝗿𝗻𝗲𝗰𝗲𝗿 𝘂𝗺𝗮 𝗻𝗼𝘃𝗮 𝗱𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗮 𝗱𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼!**"
        )
