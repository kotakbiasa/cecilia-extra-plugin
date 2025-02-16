import io
import os
import os.path
import time
from inspect import getfullargspec
from os.path import exists, isdir

from Cecilia import app
from Cecilia.misc import SUDOERS
from pyrogram import filters
from pyrogram.types import Message

from utils.error import capture_err

MAX_MESSAGE_SIZE_LIMIT = 4095


@app.on_message(filters.command("ls") & ~filters.forwarded & ~filters.via_bot & SUDOERS)
@capture_err
async def lst(_, message: Message):
    prefix = message.text.split()[0][0]
    chat_id = message.chat.id
    path = os.getcwd()
    text = message.text.split(" ", 1)
    directory = None
    if len(text) > 1:
        directory = text[1].strip()
        path = directory
    if not exists(path):
        await eor(
            message,
            text=f"❌ **𝗡𝗮̃𝗼 𝗲𝘅𝗶𝘀𝘁𝗲 𝗻𝗲𝗻𝗵𝘂𝗺 𝗱𝗶𝗿𝗲𝘁𝗼́𝗿𝗶𝗼 𝗼𝘂 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗰𝗼𝗺 𝗼 𝗻𝗼𝗺𝗲** `{directory}`. 𝗩𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲!",
        )
        return
    if isdir(path):
        if directory:
            msg = f"📁 **𝗣𝗮𝘀𝘁𝗮𝘀 𝗲 𝗔𝗿𝗾𝘂𝗶𝘃𝗼𝘀 𝗲𝗺** `{path}` :\n\n"
            lists = os.listdir(path)
        else:
            msg = "📂 **𝗣𝗮𝘀𝘁𝗮𝘀 𝗲 𝗔𝗿𝗾𝘂𝗶𝘃𝗼𝘀 𝗻𝗼 𝗗𝗶𝗿𝗲𝘁𝗼́𝗿𝗶𝗼 𝗔𝘁𝘂𝗮𝗹:**\n\n"
            lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            thepathoflight = path + "/" + contents
            if not isdir(thepathoflight):
                size = os.stat(thepathoflight).st_size
                if contents.endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += "🎵 " + f"`{contents}`\n"
                elif contents.endswith((".opus")):
                    files += "🎙 " + f"`{contents}`\n"
                elif contents.endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
                    files += "🎞 " + f"`{contents}`\n"
                elif contents.endswith((".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")):
                    files += "🗜 " + f"`{contents}`\n"
                elif contents.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")):
                    files += "🖼 " + f"`{contents}`\n"
                elif contents.endswith((".exe", ".deb")):
                    files += "⚙️ " + f"`{contents}`\n"
                elif contents.endswith((".iso", ".img")):
                    files += "💿 " + f"`{contents}`\n"
                elif contents.endswith((".apk", ".xapk")):
                    files += "📱 " + f"`{contents}`\n"
                elif contents.endswith((".py")):
                    files += "🐍 " + f"`{contents}`\n"
                else:
                    files += "📄 " + f"`{contents}`\n"
            else:
                folders += f"📁 `{contents}`\n"
        if files or folders:
            msg = msg + folders + files
        else:
            msg += "__𝗖𝗮𝗺𝗶𝗻𝗵𝗼 𝘃𝗮𝘇𝗶𝗼__"
    else:
        size = os.stat(path).st_size
        msg = "📄 **𝗗𝗲𝘁𝗮𝗹𝗵𝗲𝘀 𝗱𝗼 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗱𝗼:**\n\n"
        if path.endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵 "
        elif path.endswith((".opus")):
            mode = "🎙 "
        elif path.endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞 "
        elif path.endswith((".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")):
            mode = "🗜 "
        elif path.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")):
            mode = "🖼 "
        elif path.endswith((".exe", ".deb")):
            mode = "⚙️ "
        elif path.endswith((".iso", ".img")):
            mode = "💿 "
        elif path.endswith((".apk", ".xapk")):
            mode = "📱 "
        elif path.endswith((".py")):
            mode = "🐍 "
        else:
            mode = "📄 "
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**📍 𝗟𝗼𝗰𝗮𝗹𝗶𝘇𝗮𝗰̧𝗮̃𝗼:** `{path}`\n"
        msg += f"**🔖 𝗜́𝗰𝗼𝗻𝗲:** `{mode}`\n"
        msg += f"**📏 𝗧𝗮𝗺𝗮𝗻𝗵𝗼:** `{humanbytes(size)}`\n"
        msg += f"**🕒 𝗨́𝗹𝘁𝗶𝗺𝗮 𝗠𝗼𝗱𝗶𝗳𝗶𝗰𝗮𝗰̧𝗮̃𝗼:** `{time2}`\n"
        msg += f"**📅 𝗨́𝗹𝘁𝗶𝗺𝗼 𝗔𝗰𝗲𝘀𝘀𝗼:** `{time3}`"

    if len(msg) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await app.send_document(
                chat_id,
                out_file,
                caption=path,
            )
            await message.delete()
    else:
        await eor(message, text=msg)


@app.on_message(filters.command("rm") & ~filters.forwarded & ~filters.via_bot & SUDOERS)
@capture_err
async def rm_file(_, message: Message):
    if len(message.command) < 2:
        return await eor(message,
                         text="🚫 **𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝗼 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝗺 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗽𝗮𝗿𝗮 𝗱𝗲𝗹𝗲𝘁𝗮𝗿.**")
    file = message.text.split(" ", 1)[1]
    if exists(file):
        os.remove(file)
        await eor(message, text=f"🗑️ **{file} 𝗳𝗼𝗶 𝗱𝗲𝗹𝗲𝘁𝗮𝗱𝗼.**")
    else:
        await eor(message, text=f"❌ **{file} 𝗻𝗮̃𝗼 𝗲𝘅𝗶𝘀𝘁𝗲!**")


async def eor(msg: Message, **kwargs: dict):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
