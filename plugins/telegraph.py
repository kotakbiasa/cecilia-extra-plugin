import os

from TheApi import api
from Cecilia import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗱𝗲 𝗺𝗶́𝗱𝗶𝗮 𝗽𝗮𝗿𝗮 𝗳𝗮𝘇𝗲𝗿 𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵 📤"
        )

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    if file_size > 15 * 1024 * 1024:
        return await message.reply_text(
            "𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗲𝗻𝘃𝗶𝗲 𝘂𝗺 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗱𝗲 𝗺𝗲́𝗱𝗶𝗮 𝗱𝗲 𝗮𝘁𝗲́ 𝟭𝟱𝗠𝗕 ⚠️.")

    try:
        text = await message.reply("𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼... 🔄")

        async def progress(current, total):
            try:
                await text.edit_text(f"📥 𝗕𝗮𝗶𝘅𝗮𝗻𝗱𝗼... {current * 100 / total:.1f}%")
            except Exception:
                pass

        try:
            local_path = await media.download(progress=progress)
            await text.edit_text("📤 𝗙𝗮𝘇𝗲𝗻𝗱𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗽𝗮𝗿𝗮 𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵...")

            upload_path = api.upload_image(local_path)

            await text.edit_text(
                f"🌐 | [𝗟𝗶𝗻𝗸 𝗱𝗲 𝗨𝗽𝗹𝗼𝗮𝗱]({upload_path})",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "𝗔𝗿𝗾𝘂𝗶𝘃𝗼 𝗲𝗻𝘃𝗶𝗮𝗱𝗼 📂",
                                url=upload_path,
                            )
                        ]
                    ]
                ),
            )

            try:
                os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            await text.edit_text(f"❌ 𝗙𝗮𝗹𝗵𝗮 𝗻𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗱𝗼 𝗮𝗿𝗾𝘂𝗶𝘃𝗼\n\n<i>𝗥𝗮𝘇𝗮̃𝗼: {e}</i>")
            try:
                os.remove(local_path)
            except Exception:
                pass
            return
    except Exception:
        pass


__MODULE__ = "📎𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵"
__HELP__ = """
**𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗼 𝗕𝗼𝘁 𝗱𝗲 𝗨𝗽𝗹𝗼𝗮𝗱 𝗱𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵 **

𝗨𝘀𝗲 𝗲𝘀𝘁𝗲𝘀 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗽𝗮𝗿𝗮 𝗳𝗮𝘇𝗲𝗿 𝘂𝗽𝗹𝗼𝗮𝗱 𝗱𝗲 𝗮𝗿𝗾𝘂𝗶𝘃𝗼𝘀 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵:

- `/tgm`: 𝗳𝗮𝘇 𝘂𝗽𝗹𝗼𝗮𝗱 𝗱𝗲 𝗺𝗶́𝗱𝗶𝗮 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗶𝗱𝗮 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵.
- `/tgt`: 𝗺𝗲𝘀𝗺𝗼 𝗾𝘂𝗲 `/tgm`.
- `/telegraph`: 𝗺𝗲𝘀𝗺𝗼 𝗾𝘂𝗲 `/tgm`.
- `/tl`: 𝗺𝗲𝘀𝗺𝗼 𝗾𝘂𝗲 `/tgm`.

**𝗘𝘅𝗲𝗺𝗽𝗹𝗼:**
- 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗼𝘂 𝘃𝗶́𝗱𝗲𝗼 𝗰𝗼𝗺 `/tgm` 𝗽𝗮𝗿𝗮 𝗳𝗮𝘇𝗲𝗿 𝗼 𝘂𝗽𝗹𝗼𝗮𝗱.

**𝗔𝘃𝗶𝘀𝗼:**
𝗩𝗼𝗰𝗲̂ 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗿 𝘂𝗺 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗱𝗲 𝗺𝗶́𝗱𝗶𝗮 𝗽𝗮𝗿𝗮 𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮𝗿.
"""
