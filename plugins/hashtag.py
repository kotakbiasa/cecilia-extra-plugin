from TheApi import api
from WinxMusic import app
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command("hashtag"))
async def hashtag(_, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        res = api.gen_hashtag(text)
    except IndexError:
        return await message.reply_text("**Exemplo:**\n\n`/hashtag python`")

    await message.reply_text(f"**Aqui está sua hashtag:**\n<pre>{res}</pre>", quote=True)


__MODULE__ = "#️⃣𝗛𝗮𝘀𝗵𝘁𝗮𝗴"
__HELP__ = """
**𝗚𝗲𝗿𝗮𝗱𝗼𝗿 𝗱𝗲 𝗛𝗮𝘀𝗵𝘁𝗮𝗴𝘀:**

• `/hashtag [texto]`: 𝗚𝗲𝗿𝗮 𝗵𝗮𝘀𝗵𝘁𝗮𝗴𝘀 𝗽𝗮𝗿𝗮 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗱𝗶𝗴𝗶𝘁𝗮𝗱𝗼.
"""
