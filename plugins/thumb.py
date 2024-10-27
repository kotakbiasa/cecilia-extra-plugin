import re

from WinxMusic import app
from pyrogram import filters
from youtubesearchpython.__future__ import VideosSearch


async def gen_infos(url):
    results = VideosSearch(url, limit=1)
    for result in (await results.next())["result"]:
        title = result["title"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return title, thumbnail


def is_url(url):
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.match(regex, url)
    if match:
        return True, match.group(1)
    return False, None


@app.on_message(
    filters.command(["getthumb", "genthumb", "thumb", "thumbnail"], prefixes="/")
)
async def get_thumbnail_command(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "𝗙𝗼𝗿𝗻𝗲𝗰̧𝗮 𝗺𝗲 𝘂𝗺 𝗹𝗶𝗻𝗸 𝗱𝗲 𝘃𝗶́𝗱𝗲𝗼 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝗱𝗲𝗽𝗼𝗶𝘀 𝗱𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗮 𝗺𝗶𝗻𝗶𝗮𝘁𝘂𝗿𝗮 📷"
        )
    try:
        a = await message.reply_text("𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼... ⏳")
        url = message.text.split(" ")[1]
        i, video_id = is_url(url)
        if not i:
            return await a.edit("𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝗹𝗶𝗻𝗸 𝘃𝗮́𝗹𝗶𝗱𝗼 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲. 🔗")

        title, thumb = await gen_infos(url)
        caption = f"<b>[{title}](https://t.me/{app.username}?start=info_{video_id})</b>"
        await message.reply_photo(thumb, caption=caption)
        await a.delete()
    except Exception as e:
        await a.edit(f"𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼𝗿: {e} ❌")


__MODULE__ = "📷𝗬𝗧𝗠𝗶𝗻𝗶𝗮𝘁𝘂𝗿𝗮"
__HELP__ = """
**𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗼 𝗯𝗼𝘁 𝗱𝗲 𝗺𝗶𝗻𝗶𝗮𝘁𝘂𝗿𝗮 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 📺**

𝗨𝘁𝗶𝗹𝗶𝘇𝗲 𝗲𝘀𝘀𝗲𝘀 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗮 𝗺𝗶𝗻𝗶𝗮𝘁𝘂𝗿𝗮 𝗱𝗲 𝘂𝗺 𝘃𝗶́𝗱𝗲𝗼 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲:

- /getthumb <𝗹𝗶𝗻𝗸_𝘆𝘁>: 𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝗮 𝗺𝗶𝗻𝗶𝗮𝘁𝘂𝗿𝗮 𝗱𝗲 𝘂𝗺 𝘃𝗶́𝗱𝗲𝗼 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 🖼️.

- /genthumb <𝗹𝗶𝗻𝗸_𝘆𝘁>: 𝗠𝗲𝘀𝗺𝗮 𝗳𝘂𝗻𝗰̧𝗮̃𝗼 𝗱𝗲 /getthumb.

- /thumb <𝗹𝗶𝗻𝗸_𝘆𝘁>: 𝗠𝗲𝘀𝗺𝗮 𝗳𝘂𝗻𝗰̧𝗮̃𝗼 𝗱𝗲 /getthumb.

- /thumbnail <𝗹𝗶𝗻𝗸_𝘆𝘁>: 𝗠𝗲𝘀𝗺𝗮 𝗳𝘂𝗻𝗰̧𝗮̃𝗼 𝗱𝗲 /getthumb.

**𝗘𝘅𝗲𝗺𝗽𝗹𝗼:**
- `/getthumb https://www.youtube.com/watch?v=Tl4bQBfOtbg`

**𝗡𝗼𝘁𝗮:**
𝗙𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝗹𝗶𝗻𝗸 𝘃𝗮́𝗹𝗶𝗱𝗼 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝗱𝗲𝗽𝗼𝗶𝘀 𝗱𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗮 𝗺𝗶𝗻𝗶𝗮𝘁𝘂𝗿𝗮.
"""
