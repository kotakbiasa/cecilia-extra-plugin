from WinxMusic import app
from WinxMusic.utils import Yukkibin
from WinxMusic.utils.database import get_assistant, get_lang
from pyrogram import filters
from pyrogram.enums import ChatType
from strings import get_string


@app.on_message(
    filters.command(["vcuser", "vcusers", "vcmember", "vcmembers"]) & filters.admin
)
async def vc_members(client, message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("pt_br")
    msg = await message.reply_text(
        "🚫 𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲! 𝗢 𝗯𝗼𝘁 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝘂𝗺 𝗻𝘂́𝗺𝗲𝗿𝗼 𝗹𝗶𝗺𝗶𝘁𝗮𝗱𝗼 𝗱𝗲 𝘃𝗶𝗱𝗲𝗼𝗰𝗵𝗮𝗺𝗮𝗱𝗮𝘀 𝗱𝗲𝘃𝗶𝗱𝗼 𝗮 𝗽𝗿𝗼𝗯𝗹𝗲𝗺𝗮𝘀 𝗱𝗲 𝘀𝗼𝗯𝗿𝗲𝗰𝗮𝗿𝗴𝗮 𝗱𝗮 𝗖𝗣𝗨. 𝗠𝘂𝗶𝘁𝗼𝘀 𝗼𝘂𝘁𝗿𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗲𝘀𝘁𝗮̃𝗼 𝘂𝘀𝗮𝗻𝗱𝗼 𝘃𝗶𝗱𝗲𝗼𝗰𝗵𝗮𝗺𝗮𝗱𝗮 𝗻𝗼 𝗺𝗼𝗺𝗲𝗻𝘁𝗼. 𝗧𝗲𝗻𝘁𝗲 𝗺𝘂𝗱𝗮𝗿 𝗽𝗮𝗿𝗮 𝗮́𝘂𝗱𝗶𝗼 𝗼𝘂 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲. 🎙️")

    userbot = await get_assistant(message.chat.id)
    TEXT = ""

    try:
        async for m in userbot.get_call_members(message.chat.id):
            chat_id = m.chat.id
            username = m.chat.username
            is_hand_raised = "🙋‍♂️" if m.is_hand_raised else "✋"
            is_video_enabled = "📹" if m.is_video_enabled else "📵"
            is_left = "🚶‍♂️" if m.is_left else "🔊"
            is_screen_sharing_enabled = "🖥️" if m.is_screen_sharing_enabled else "❌"
            is_muted = "🔇" if bool(m.is_muted and not m.can_self_unmute) else "🔈"
            is_speaking = "💬" if not m.is_muted else "🤐"

            if m.chat.type != ChatType.PRIVATE:
                title = m.chat.title
            else:
                try:
                    title = (await client.get_users(chat_id)).mention
                except:
                    title = m.chat.first_name

            TEXT += f"𝗨𝘀𝘂𝗮́𝗿𝗶𝗼: {title}\n𝗜𝗗: {chat_id}\n👤 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}\n📹 𝗩𝗶́𝗱𝗲𝗼: {is_video_enabled}\n🖥️ 𝗖𝗼𝗺𝗽𝗮𝗿𝘁𝗶𝗹𝗵𝗮𝗻𝗱𝗼 𝗲𝗿𝗮𝗻: {is_screen_sharing_enabled}\n🙋 𝗠𝗮̃𝗼 𝗹𝗲𝘃𝗮𝗻𝘁𝗮𝗱𝗮: {is_hand_raised}\n🔈 𝗠𝘂𝗱𝗼: {is_muted}\n💬 𝗙𝗮𝗹𝗮𝗻𝗱𝗼: {is_speaking}\n🚶 𝗦𝗮𝗶𝘂: {is_left}\n\n"

        if len(TEXT) < 4000:
            await msg.edit(TEXT or "⚠️ 𝗡𝗲𝗻𝗵𝘂𝗺 𝗺𝗲𝗺𝗯𝗿𝗼 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗱𝗼.")
        else:
            link = await Yukkibin(TEXT)
            await msg.edit(
                f"📄 𝗟𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗹𝗶𝘀𝘁𝗮: {link}",
                disable_web_page_preview=True,
            )
    except ValueError as e:
        await msg.edit("❗ 𝗘𝗿𝗿𝗼𝗿𝗲: 𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗰𝗮𝗿𝗿𝗲𝗴𝗮𝗿 𝗮 𝗹𝗶𝘀𝘁𝗮.")
