import nekos
from WinxMusic import app
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command("hug"))
async def hug(_, message: Message):
    try:
        if message.reply_to_message:
            await message.reply_video(
                nekos.img("hug"),
                caption=f"{message.from_user.mention} abraçou {message.reply_to_message.from_user.mention} 🤗",
            )
        else:
            await message.reply_video(nekos.img("hug"), caption="Um abraço para você! 🤗")
    except Exception as e:
        await message.reply_text(f"Erro: {e}")


__MODULE__ = "🫂𝗔𝗯𝗿𝗮𝗰̧𝗼"
__HELP__ = """
**𝗖𝗼𝗺𝗮𝗻𝗱𝗼 𝗱𝗲 𝗔𝗯𝗿𝗮𝗰̧𝗼:**

- `/hug`: Envia uma animação de abraço. Se usado como resposta a uma mensagem, menciona quem enviou e quem recebeu o abraço.

**𝗜𝗻𝘀𝘁𝗿𝘂𝗰̧𝗼̃𝗲𝘀:**

- Use `/hug` para enviar um abraço animado.
- Responda a uma mensagem com `/hug` para enviar um abraço mencionando o remetente e o destinatário.

**𝗜𝗺𝗽𝗼𝗿𝘁𝗮𝗻𝘁𝗲:**

- Verifique se as configurações do seu chat permitem que o bot envie vídeos para funcionamento completo.
"""
