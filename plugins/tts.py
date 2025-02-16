import io

from Cecilia import app
from gtts import gTTS
from pyrogram import filters


@app.on_message(filters.command("tts"))
async def text_to_speech(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰𝗮 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗲𝗿𝘁𝗲𝗿 𝗲𝗺 𝗮𝘂́𝗱𝗶𝗼. 🎤"
        )

    text = message.text.split(None, 1)[1]
    tts = gTTS(text, lang="pt")
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)

    audio_file = io.BytesIO(audio_data.read())
    audio_file.name = "audio.mp3"
    await message.reply_audio(audio_file)


__MODULE__ = "🎧𝗧𝗧𝘀"
__HELP__ = """
**📢 𝗖𝗼𝗺𝗮𝗻𝗱𝗼 𝗱𝗲 𝗧𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗔𝘂́𝗱𝗶𝗼 🎶**

𝗨𝘁𝗶𝗹𝗶𝘇𝗲 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 `/tts` 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗲𝗿𝘁𝗲𝗿 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗲𝗺 𝗮𝘂́𝗱𝗶𝗼 𝗲𝗺 𝗽𝗼𝗿𝘁𝘂𝗴𝘂𝗲̂𝘀.

- `/tts <𝘁𝗲𝘅𝘁𝗼>`: 𝗰𝗼𝗻𝘃𝗲𝗿𝘁𝗲 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗱𝗶𝗴𝗶𝘁𝗮𝗱𝗼 𝗲𝗺 𝗮𝘂́𝗱𝗶𝗼 𝗲𝗺 𝗽𝗼𝗿𝘁𝘂𝗴𝘂𝗲̂𝘀. 🇧🇷

**📝 𝗘𝘅𝗲𝗺𝗽𝗹𝗼:**
- `/tts Olá Mundo`

**⚠️ 𝗡𝗼𝘁𝗮:**
𝗖𝗲𝗿𝘁𝗶𝗳𝗶𝗾𝘂𝗲-𝘀𝗲 𝗱𝗲 𝗳𝗼𝗿𝗻𝗲𝗰𝗲𝗿 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 `/tts`.
"""
