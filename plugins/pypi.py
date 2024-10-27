import requests
from WinxMusic import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_pypi_info(package_name):
    try:
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(api_url)
        if response.status_code == 200:
            pypi_info = response.json()
            return pypi_info
        else:
            return None
    except Exception as e:
        print(f"Error fetching PyPI information: {e}")
        return None


@app.on_message(filters.command("pypi", prefixes="/"))
async def pypi_info_command(client, message):
    try:
        package_name = message.command[1]
        pypi_info = get_pypi_info(package_name)

        if pypi_info:
            info_message = (
                f"𝗖𝗮𝗿𝗼 {message.from_user.mention} 👋\n"
                "📦 𝗔𝗾𝘂𝗶 𝗲𝘀𝘁𝗮̃𝗼 𝗼𝘀 𝗱𝗲𝘁𝗮𝗹𝗵𝗲𝘀 𝗱𝗼 𝘀𝗲𝘂 𝗽𝗮𝗰𝗼𝘁𝗲:\n\n"
                f"📛 𝗡𝗼𝗺𝗲 𝗱𝗼 𝗽𝗮𝗰𝗼𝘁𝗲 ➪ {pypi_info['info']['name']}\n\n"
                f"🔢 𝗨́𝗹𝘁𝗶𝗺𝗮 𝘃𝗲𝗿𝘀𝗮̃𝗼 ➪ {pypi_info['info']['version']}\n\n"
                f"📝 𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼 ➪ {pypi_info['info']['summary']}\n\n"
                f"🔗 𝗨𝗥𝗟 𝗱𝗼 𝗽𝗿𝗼𝗷𝗲𝘁𝗼 ➪ {pypi_info['info']['project_urls']['Homepage']}"
            )
            close_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="〆 𝗙𝗲𝗰𝗵𝗮𝗿 〆", callback_data="close")]]
            )
            await message.reply_text(info_message, reply_markup=close_markup)
        else:
            await message.reply_text(
                f"⚠️ 𝗣𝗮𝗰𝗼𝘁𝗲 '{package_name}' 𝗻𝗮̃𝗼 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗱𝗼 \n𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
            )

    except IndexError:
        await message.reply_text(
            "ℹ️ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝗻𝗼𝗺𝗲 𝗱𝗲 𝗽𝗮𝗰𝗼𝘁𝗲 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /pypi."
        )


__MODULE__ = "🐍𝗣𝘆𝗣𝗶"
__HELP__ = """
**💻 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀:**
• `/pypi <nome_do_pacote>`: Obtenha detalhes sobre um pacote Python específico do PyPI.

**ℹ️ 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀:**
𝗘𝘀𝘁𝗲 𝗺𝗼́𝗱𝘂𝗹𝗼 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗾𝘂𝗲 𝗼𝘀 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗯𝘂𝘀𝗾𝘂𝗲𝗺 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗽𝗮𝗰𝗼𝘁𝗲𝘀 𝗣𝘆𝘁𝗵𝗼𝗻 𝗱𝗼 𝗣𝘆𝗣𝗶, 𝗶𝗻𝗰𝗹𝘂𝗶𝗻𝗱𝗼 𝗼 𝗻𝗼𝗺𝗲 𝗱𝗼 𝗽𝗮𝗰𝗼𝘁𝗲, 𝘂́𝗹𝘁𝗶𝗺𝗮 𝘃𝗲𝗿𝘀𝗮̃𝗼, 𝗱𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼 𝗲 𝗨𝗥𝗟 𝗱𝗼 𝗽𝗿𝗼𝗷𝗲𝘁𝗼.

**📝 𝗡𝗼𝘁𝗮:**
𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝗻𝗼𝗺𝗲 𝗱𝗲 𝗽𝗮𝗰𝗼𝘁𝗲 𝘃𝗮́𝗹𝗶𝗱𝗼 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 `/pypi` 𝗽𝗮𝗿𝗮 𝗿𝗲𝗰𝘂𝗽𝗲𝗿𝗮𝗿 𝗱𝗲𝘁𝗮𝗹𝗵𝗲𝘀 𝗱𝗼 𝗽𝗮𝗰𝗼𝘁𝗲.
"""
