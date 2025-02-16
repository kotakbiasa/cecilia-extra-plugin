import logging

from SafoneAPI import SafoneAPI
from Cecilia import app
from googlesearch import search
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command(["google", "gle"]))
async def google(_, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("Exemplo:\n\n`/google exemplo de pesquisa`")
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])
    b = await message.reply_text("𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...🔎")
    try:
        a = search(user_input, advanced=True)
        txt = f"𝗤𝘂𝗲𝗿𝘆 𝗱𝗲 𝗕𝘂𝘀𝗰𝗮: {user_input}\n\nResultados:"
        for result in a:
            txt += f"\n\n[❍ {result.title}]({result.url})\n<b>{result.description}</b>"
        await b.edit(
            txt,
            disable_web_page_preview=True,
        )
    except Exception as e:
        await b.edit(f"𝗙𝗮𝗹𝗵𝗮: {str(e)} ❌")
        logging.exception(e)


@app.on_message(filters.command(["app", "apps"]))
async def app(_, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("Exemplo:\n\n`/app Nome do App`")
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])
    cbb = await message.reply_text("𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼 𝗻𝗼 𝗣𝗹𝗮𝘆 𝗦𝘁𝗼𝗿𝗲...📱")
    a = await SafoneAPI().apps(user_input, 1)
    b = a["results"][0]
    icon = b["icon"]
    id = b["id"]
    link = b["link"]
    ca = b["description"]
    title = b["title"]
    dev = b["developer"]
    info = f"<b>[𝗧𝗶𝘁𝘂𝗹𝗼 : {title}]({link})</b>\n<b>𝗜𝗗</b>: <code>{id}</code>\n<b>𝗗𝗲𝘀𝗲𝗻𝘃𝗼𝗹𝘃𝗲𝗱𝗼𝗿</b> : {dev}\n<b>𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼</b>: {ca}"
    try:
        await message.reply_photo(icon, caption=info)
        await cbb.delete()
    except Exception as e:
        await message.reply_text(f"𝗘𝗿𝗿𝗼: {str(e)} ❌")


__MODULE__ = "🌐𝗚𝗼𝗼𝗴𝗹𝗲"
__HELP__ = """
/google [𝘲𝘶𝘦𝘳𝘺] - 𝗽𝗮𝗿𝗮 𝗯𝘂𝘀𝗰𝗮𝗿 𝗻𝗼 𝗚𝗼𝗼𝗴𝗹𝗲 𝗲 𝗼𝗯𝘁𝗲𝗿 𝗿𝗲𝘀𝘂𝗹𝘁𝗮𝗱𝗼𝘀
/app | /apps [𝗻𝗼𝗺𝗲 𝗱𝗼 𝗮𝗽𝗽] - 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗮̃𝗼 𝗱𝗼 𝗮𝗽𝗽 𝗱𝗶𝘀𝗽𝗼𝗻𝗶𝘃𝗲𝗹 𝗻𝗼 𝗣𝗹𝗮𝘆𝗦𝘁𝗼𝗿𝗲
"""
