from Cecilia import app
from pyrogram import filters


@app.on_message(filters.command(["qr"]))
async def write_text(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "**𝗨𝘀𝗮𝗴𝗲**: ➡️ `/qr https://t.me/vivekkumar07089`\n📌 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗹𝗶𝗻𝗸 𝗼𝗿 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗮 𝗤𝗥 𝗖𝗼𝗱𝗲.")
        return
    text = " ".join(message.command[1:])
    photo_url = "https://apis.xditya.me/qr/gen?text=" + text
    await app.send_photo(
        chat_id=message.chat.id, photo=photo_url, caption="✅ 𝗛𝗲𝗿𝗲 𝗶𝘀 𝘆𝗼𝘂𝗿 𝗤𝗥 𝗖𝗼𝗱𝗲! 📲"
    )


__MODULE__ = "✨𝗤𝗥 𝗖𝗼𝗱𝗲"

__HELP__ = """
🤖 **𝗧𝗵𝗶𝘀 𝗺𝗼𝗱𝘂𝗹𝗲 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝘀 𝗤𝗥 𝗰𝗼𝗱𝗲𝘀.**

🔹 **𝗨𝘀𝗲 𝘁𝗵𝗲 /qr 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗳𝗼𝗹𝗹𝗼𝘄𝗲𝗱 𝗯𝘆 𝘁𝗵𝗲 𝘁𝗲𝘅𝘁 𝗼𝗿 𝗨𝗥𝗟 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗲𝗻𝗰𝗼𝗱𝗲 𝗶𝗻𝘁𝗼 𝗮 𝗤𝗥 𝗖𝗼𝗱𝗲.**

📌 **𝗙𝗼𝗿 𝗲𝘅𝗮𝗺𝗽𝗹𝗲**: `/qr https://t.me/vivekkumar07089`

🔍 𝗧𝗵𝗲 𝗯𝗼𝘁 𝘄𝗶𝗹𝗹 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗮 𝗤𝗥 𝗖𝗼𝗱𝗲 𝗳𝗼𝗿 𝘁𝗵𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲𝗱 𝗶𝗻𝗽𝘂𝘁.

⚠️ **𝗡𝗼𝘁𝗲**: 𝗠𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝘁𝗼 𝗶𝗻𝗰𝗹𝘂𝗱𝗲 𝘁𝗵𝗲 𝗽𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (`http://` 𝗼𝗿 `https://`) 𝗳𝗼𝗿 𝗨𝗥𝗟𝘀.

🎉 𝗘𝗻𝗷𝗼𝘆 𝗰𝗿𝗲𝗮𝘁𝗶𝗻𝗴 𝗤𝗥 𝗖𝗼𝗱𝗲𝘀 𝘄𝗶𝘁𝗵 𝗲𝗮𝘀𝗲!
"""
