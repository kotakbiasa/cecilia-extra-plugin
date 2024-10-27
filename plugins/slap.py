import nekos
from WinxMusic import app
from pyrogram import filters


@app.on_message(filters.command("slap"))
async def slap(client, message):
    try:
        if message.reply_to_message:
            await message.reply_video(
                nekos.img("slap"),
                caption=f"💥 {message.from_user.mention} 𝗱𝗲𝘂 𝘂𝗺 𝘁𝗮𝗽𝗮 𝗲𝗺 {message.reply_to_message.from_user.mention}! 💥",
            )
        else:
            await message.reply_video(nekos.img("slap"))
    except Exception as e:
        await message.reply_text(f"⚠️ 𝗘𝗿𝗿𝗼: {e}")


__MODULE__ = "💥𝗧𝗮𝗽𝗮"
__HELP__ = """
📋 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗶𝘀:
- /slap: 𝗗𝗮 𝘂𝗺 𝘁𝗮𝗽𝗮 𝗲𝗺 𝗮𝗹𝗴𝘂𝗲𝗺. 𝗦𝗲 𝘂𝘀𝗮𝗱𝗼 𝗰𝗼𝗺𝗼 𝗿𝗲𝘀𝗽𝗼𝘀𝘁𝗮, 𝗱𝗮 𝘂𝗺 𝘁𝗮𝗽𝗮 𝗻𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗶𝗱𝗼.
"""
