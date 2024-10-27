from TheApi import api
from WinxMusic import app
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command(["write"]))
async def write(_, message: Message):
    if message.reply_to_message and message.reply_to_message.text:
        txt = message.reply_to_message.text
    elif len(message.command) > 1:
        txt = message.text.split(None, 1)[1]
    else:
        return await message.reply(
            "💡 **Por favor, responda a uma mensagem ou escreva após o comando para usar o comando /write.**"
        )
    nan = await message.reply_text("🖊️ **Processando...**")
    try:
        img = api.write(txt)
        await message.reply_photo(img)
        await nan.delete()
    except Exception as e:
        await nan.edit(f"❌ **Erro:** {e}")


__MODULE__ = "🖋️ 𝗘𝘀𝗰𝗿𝗶𝘁𝗮"
__HELP__ = """
**🖋️ Comandos**:
- /write - **Escreva um texto em uma imagem editada.**

**📄 Informações**:
- 𝗡𝗼𝗺𝗲 𝗱𝗼 𝗠𝗼́𝗱𝘂𝗹𝗼: Escrita
- 𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼: Escreva texto em uma imagem e receba uma foto editada.
- 𝗖𝗼𝗺𝗮𝗻𝗱𝗼: /write
- 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗻𝗲𝗰𝗲𝘀𝘀𝗮́𝗿𝗶𝗮: Nenhuma

**📝 Nota**:
- Use diretamente no chat do grupo para melhores resultados.
"""
