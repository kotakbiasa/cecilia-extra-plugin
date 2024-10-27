from WinxMusic import app
from WinxMusic.core.mongo import mongodb
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.keyboard import ikb
from pyrogram import filters, Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors.exceptions.bad_request_400 import UserAlreadyParticipant
from pyrogram.types import ChatJoinRequest, Message, CallbackQuery

from utils.permissions import admins_only, member_permissions

approvaldb = mongodb.autoapprove


def smallcap(text):
    trans_table = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ0𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    )
    return text.translate(trans_table)


@app.on_message(filters.command("autoapprove") & filters.group)
@admins_only("can_change_info")
async def approval_command(_client: Client, message: Message):
    chat_id = message.chat.id
    chat = await approvaldb.find_one({"chat_id": chat_id})
    if chat:
        mode = chat.get("mode", "")
        if not mode:
            mode = "manual"
            await approvaldb.update_one(
                {"chat_id": chat_id},
                {"$set": {"mode": mode}},
                upsert=True,
            )
        if mode == "automatic":
            switch = "manual"
            mdbutton = "🔄 **𝗔𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗼**"
        else:
            switch = "automatic"
            mdbutton = "🔄 **𝗠𝗮𝗻𝘂𝗮𝗹**"
        buttons = {
            "❌ **𝗗𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗿**": "approval_off",
            f"{mdbutton}": f"approval_{switch}",
        }
        keyboard = ikb(buttons, 1)
        await message.reply(
            "✅ **𝗔𝗽𝗿𝗼𝘃𝗮𝗰̧𝗮̃𝗼 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗮 𝗮𝘁𝗶𝘃𝗮𝗱𝗮 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼.**", reply_markup=keyboard
        )
    else:
        buttons = {"✅ **𝗔𝘁𝗶𝘃𝗮𝗿**": "approval_on"}
        keyboard = ikb(buttons, 1)
        await message.reply(
            "❌ **𝗔𝗽𝗿𝗼𝘃𝗮𝗰̧𝗮̃𝗼 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗮 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗱𝗮 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼.**", reply_markup=keyboard
        )


@app.on_callback_query(filters.regex("approval(.*)"))
async def approval_cb(_client: Client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    from_user = callback_query.from_user
    permissions = await member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        if from_user.id not in SUDOERS:
            return await callback_query.answer(
                f"❌ **𝗩𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝗽𝗼𝘀𝘀𝘂𝗶 𝗮 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗻𝗲𝗰𝗲𝘀𝘀𝗮́𝗿𝗶𝗮.**\n**𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼:** {permission}",
                show_alert=True,
            )
    command_parts = callback_query.data.split("_", 1)
    option = command_parts[1]
    if option == "off":
        if await approvaldb.count_documents({"chat_id": chat_id}) > 0:
            approvaldb.delete_one({"chat_id": chat_id})
            buttons = {"✅ **𝗔𝘁𝗶𝘃𝗮𝗿**": "approval_on"}
            keyboard = ikb(buttons, 1)
            return await callback_query.edit_message_text(
                "❌ **𝗔𝗽𝗿𝗼𝘃𝗮𝗰̧𝗮̃𝗼 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗮 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗱𝗮 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼.**",
                reply_markup=keyboard,
            )
    if option == "on":
        switch = "manual"
        mode = "automatic"
    if option == "automatic":
        switch = "manual"
        mode = option
    if option == "manual":
        switch = "automatic"
        mode = option
    await approvaldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )
    chat = await approvaldb.find_one({"chat_id": chat_id})
    mode = "🔄 **𝗔𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗼**" if chat["mode"] == "automatic" else "🔄 **𝗠𝗮𝗻𝘂𝗮𝗹**"
    buttons = {"❌ **𝗗𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗿**": "approval_off", f"{mode}": f"approval_{switch}"}
    keyboard = ikb(buttons, 1)
    await callback_query.edit_message_text(
        "✅ **𝗔𝗽𝗿𝗼𝘃𝗮𝗰̧𝗮̃𝗼 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗮 𝗮𝘁𝗶𝘃𝗮𝗱𝗮 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼.**", reply_markup=keyboard
    )


@app.on_message(filters.command("approveall") & filters.group)
@admins_only("can_restrict_members")
async def clear_pending_command(_client: Client, message: Message):
    a = await message.reply_text("⏳ **𝗔𝗴𝘂𝗮𝗿𝗱𝗲...**")
    chat_id = message.chat.id
    await app.approve_all_chat_join_requests(chat_id)
    await a.edit(
        "✅ **𝗦𝗲 𝗵𝗮́ 𝗮𝗹𝗴𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗮𝗴𝘂𝗮𝗿𝗱𝗮𝗻𝗱𝗼 𝗮𝗽𝗿𝗼𝘃𝗮𝗰̧𝗮̃𝗼, 𝗲𝘂 𝗷𝗮́ 𝗼 𝗮𝗽𝗿𝗼𝘃𝗲𝗶.**")
    await approvaldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"pending_users": []}},
    )


@app.on_message(filters.command("clearpending") & filters.group)
@admins_only("can_restrict_members")
async def clear_pending_command(_client: Client, message: Message):
    chat_id = message.chat.id
    result = await approvaldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"pending_users": []}},
    )
    if result.modified_count > 0:
        await message.reply_text("✅ **𝗨𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗲𝗻𝗱𝗲𝗻𝘁𝗲𝘀 𝗳𝗼𝗿𝗮𝗺 𝗹𝗶𝗺𝗽𝗼𝘀.**")
    else:
        await message.reply_text("⚠️ **𝗡𝗲𝗻𝗵𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗽𝗲𝗻𝗱𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 𝗹𝗶𝗺𝗽𝗮𝗿.**")


@app.on_chat_join_request(filters.group)
async def accept(_client: Client, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user
    chat_id = await approvaldb.find_one({"chat_id": chat.id})
    if chat_id:
        mode = chat_id["mode"]
        if mode == "automatic":
            await app.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
            return
        if mode == "manual":
            is_user_in_pending = await approvaldb.count_documents(
                {"chat_id": chat.id, "pending_users": int(user.id)}
            )
            if is_user_in_pending == 0:
                await approvaldb.update_one(
                    {"chat_id": chat.id},
                    {"$addToSet": {"pending_users": int(user.id)}},
                    upsert=True,
                )
                buttons = {
                    "✅ **𝗔𝗰𝗲𝗶𝘁𝗮𝗿**": f"manual_approve_{user.id}",
                    "❌ **𝗥𝗲𝗰𝘂𝘀𝗮𝗿**": f"manual_decline_{user.id}",
                }
                keyboard = ikb(buttons, int(2))
                text = f"**𝗨𝘀𝘂𝗮́𝗿𝗶𝗼: {user.mention} 𝗲𝗻𝘃𝗶𝗼𝘂 𝘂𝗺𝗮 𝘀𝗼𝗹𝗶𝗰𝗶𝘁𝗮𝗰̧𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗽𝗮𝗿𝘁𝗶𝗰𝗶𝗽𝗮𝗿 𝗱𝗼 𝗻𝗼𝘀𝘀𝗼 𝗴𝗿𝘂𝗽𝗼. 𝗤𝘂𝗮𝗹𝗾𝘂𝗲𝗿 𝗮𝗱𝗺𝗶𝗻 𝗽𝗼𝗱𝗲 𝗮𝗰𝗲𝗶𝘁𝗮𝗿 𝗼𝘂 𝗿𝗲𝗰𝘂𝘀𝗮𝗿.**"
                admin_data = [
                    i
                    async for i in app.get_chat_members(
                        chat_id=message.chat.id,
                        filter=ChatMembersFilter.ADMINISTRATORS,
                    )
                ]
                for admin in admin_data:
                    if admin.user.is_bot or admin.user.is_deleted:
                        continue
                    text += f"[\u2063](tg://user?id={admin.user.id})"
                return await app.send_message(chat.id, text, reply_markup=keyboard)


@app.on_callback_query(filters.regex("manual_(.*)"))
async def manual(app: Client, callback_query: CallbackQuery):
    chat = callback_query.message.chat
    from_user = callback_query.from_user
    permissions = await member_permissions(chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        if from_user.id not in SUDOERS:
            return await callback_query.answer(
                f"❌ **𝗩𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝗽𝗼𝘀𝘀𝘂𝗶 𝗮 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗻𝗲𝗰𝗲𝘀𝘀𝗮́𝗿𝗶𝗮.**\n**𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼:** {permission}",
                show_alert=True,
            )
    datas = callback_query.data.split("_", 2)
    dis = datas[1]
    id = datas[2]
    if dis == "approve":
        try:
            await app.approve_chat_join_request(chat_id=chat.id, user_id=id)
        except UserAlreadyParticipant:
            await callback_query.answer(
                "✅ **𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 𝗷𝗮́ 𝗮𝗽𝗿𝗼𝘃𝗮𝗱𝗼 𝗻𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗼𝗿 𝗼𝘂𝘁𝗿𝗼 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿.**",
                show_alert=True,
            )
            return await callback_query.message.delete()

    if dis == "decline":
        try:
            await app.decline_chat_join_request(chat_id=chat.id, user_id=id)
        except Exception as e:
            if "messages.HideChatJoinRequest" in str(e):
                await callback_query.answer(
                    "✅ **𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 𝗷𝗮́ 𝗮𝗽𝗿𝗼𝘃𝗮𝗱𝗼 𝗻𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗼𝗿 𝗼𝘂𝘁𝗿𝗼 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿.**",
                    show_alert=True,
                )

    await approvaldb.update_one(
        {"chat_id": chat.id},
        {"$pull": {"pending_users": int(id)}},
    )
    return await callback_query.message.delete()


__MODULE__ = "🛡️ 𝗔𝗽𝗿𝗼𝘃𝗮𝗿"
__HELP__ = """
**Comando:** /autoapprove

🛠️ **𝗦𝗼𝗯𝗿𝗲:**  
𝗘𝘀𝘁𝗲 𝗺𝗼́𝗱𝘂𝗹𝗼 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗮 𝗮𝗽𝗿𝗼𝘃𝗮𝗰̧𝗮̃𝗼 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗮 𝗱𝗲 𝘀𝗼𝗹𝗶𝗰𝗶𝘁𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝗲𝗻𝘁𝗿𝗮𝗱𝗮 𝗲𝗺 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼 𝗮𝘁𝗿𝗮𝘃𝗲́𝘀 𝗱𝗲 𝘂𝗺 𝗹𝗶𝗻𝗸 𝗱𝗲 𝗶𝗻𝘃𝗶𝘁𝗮𝗰̧𝗮̃𝗼.

**⚙️ 𝗠𝗼𝗱𝗼𝘀:**  
𝗤𝘂𝗮𝗻𝗱𝗼 𝘃𝗼𝗰𝗲̂ 𝗲𝗻𝘃𝗶𝗮 /autoapprove 𝗻𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼, 𝘃𝗼𝗰𝗲̂ 𝗶𝗿𝗮́ 𝘃𝗲𝗿 𝘂𝗺 𝗯𝗼𝘁𝗮̃𝗼 **“𝗔𝘁𝗶𝘃𝗮𝗿”** 𝘀𝗲 𝗮 𝗮𝗽𝗿𝗼𝘃𝗮𝗰̧𝗮̃𝗼 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗮 𝗻𝗮̃𝗼 𝗲𝘀𝘁𝗶𝘃𝗲𝗿 𝗮𝘁𝗶𝘃𝗮𝗱𝗮 𝗽𝗮𝗿𝗮 𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼.  
𝗦𝗲 𝗷𝗮́ 𝗲𝘀𝘁𝗶𝘃𝗲𝗿 𝗮𝘁𝗶𝘃𝗮𝗱𝗮, 𝘃𝗼𝗰𝗲̂ 𝘃𝗲𝗿𝗮́ 𝗱𝗼𝗶𝘀 𝗺𝗼𝗱𝗼𝘀:

- **🔄 Automático** - 𝗮𝗰𝗲𝗶𝘁𝗮 𝘀𝗼𝗹𝗶𝗰𝗶𝘁𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝗲𝗻𝘁𝗿𝗮𝗱𝗮 𝗮𝘂𝘁𝗼𝗺𝗮𝘁𝗶𝗰𝗮𝗺𝗲𝗻𝘁𝗲.

- **📝 Manual** - 𝗲𝗻𝘃𝗶𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗼 𝗴𝗿𝘂𝗽𝗼, 𝗺𝗮𝗿𝗰𝗮𝗻𝗱𝗼 𝗼𝘀 𝗮𝗱𝗺𝗶𝗻𝘀, 𝗾𝘂𝗲 𝗽𝗼𝗱𝗲𝗺 𝗮𝗰𝗲𝗶𝘁𝗮𝗿 𝗼𝘂 𝗿𝗲𝗰𝘂𝘀𝗮𝗿 𝗮𝘀 𝘀𝗼𝗹𝗶𝗰𝗶𝘁𝗮𝗰̧𝗼̃𝗲𝘀.

**🧹 Usar:**  
/clearpending 𝗽𝗮𝗿𝗮 𝗹𝗶𝗺𝗽𝗮𝗿 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗲𝗻𝗱𝗲𝗻𝘁𝗲𝘀 𝗱𝗮 𝗱𝗮𝗱𝗼𝘀 𝗱𝗲 𝗲𝗻𝘁𝗿𝗮𝗱𝗮, 𝗽𝗲𝗿𝗺𝗶𝘁𝗶𝗻𝗱𝗼 𝗾𝘂𝗲 𝗲𝗹𝗲𝘀 𝗿𝗲𝗲𝗻𝘃𝗶𝗲𝗺 𝗮𝘀 𝘀𝗼𝗹𝗶𝗰𝗶𝘁𝗮𝗰̧𝗼̃𝗲𝘀.
"""
