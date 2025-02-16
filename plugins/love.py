import random

from Cecilia import app
from pyrogram import filters


def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice(
            [
                "💔 𝗢 𝗮𝗺𝗼𝗿 𝗲𝘀𝘁𝗮́ 𝗻𝗼 𝗮𝗿, 𝗺𝗮𝘀 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗱𝗲 𝘂𝗺 𝗽𝗼𝘂𝗰𝗼 𝗱𝗲 𝗲𝘀𝘁𝗶𝗺𝘂𝗹𝗼.",
                "🌱 𝗨𝗺 𝗯𝗼𝗺 𝗶́𝗻𝗶𝗰𝗶𝗼, 𝗺𝗮𝘀 𝗵𝗮́ 𝗲𝘀𝗽𝗮𝗰̧𝗼 𝗽𝗮𝗿𝗮 𝗰𝗿𝗲𝘀𝗰𝗲𝗿.",
                "✨ 𝗘́ 𝗮𝗽𝗲𝗻𝗮𝘀 𝗼 𝗶́𝗻𝗶𝗰𝗶𝗼 𝗱𝗲 𝗮𝗹𝗴𝗼 𝗯𝗲𝗹𝗼.",
            ]
        )
    elif love_percentage <= 70:
        return random.choice(
            [
                "💞 𝗛𝗮́ 𝘂𝗺𝗮 𝗳𝗼𝗿𝘁𝗲 𝗰𝗼𝗻𝗲𝘅𝗮̃𝗼. 𝗖𝗼𝗻𝘁𝗶𝗻𝘂𝗲 𝗻𝘂𝘁𝗿𝗶𝗻𝗱𝗼 𝗲𝘀𝘀𝗮 𝗿𝗲𝗹𝗮𝗰̧𝗮̃𝗼.",
                "🌼 𝗩𝗼𝗰𝗲̂𝘀 𝘁𝗲̂𝗺 𝗯𝗼𝗮𝘀 𝗰𝗵𝗮𝗻𝗰𝗲𝘀. 𝗧𝗿𝗮𝗯𝗮𝗹𝗵𝗲𝗺 𝗻𝗶𝘀𝘀𝗼.",
                "🌸 𝗢 𝗮𝗺𝗼𝗿 𝗲𝘀𝘁𝗮́ 𝗳𝗹𝗼𝗿𝗲𝘀𝗰𝗲𝗻𝗱𝗼, 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲𝗺 𝗮𝘀𝘀𝗶𝗺.",
            ]
        )
    else:
        return random.choice(
            [
                "💖 𝗨𝗮𝘂! 𝗘́ 𝘂𝗺 𝗰𝗮𝘀𝗮𝗹 𝗽𝗲𝗿𝗳𝗲𝗶𝘁𝗼!",
                "💘 𝗖𝗼𝗺𝗯𝗶𝗻𝗮𝗰̧𝗮̃𝗼 𝗽𝗲𝗿𝗳𝗲𝗶𝘁𝗮! 𝗔𝗽𝗿𝗲𝗰𝗶𝗲𝗺 𝗲𝘀𝘀𝗮 𝗹𝗶𝗴𝗮𝗰̧𝗮̃𝗼.",
                "💞 𝗗𝗲𝘀𝘁𝗶𝗻𝗮𝗱𝗼𝘀 𝗮 𝗳𝗶𝗰𝗮𝗿𝗲𝗺 𝗷𝘂𝗻𝘁𝗼𝘀. 𝗣𝗮𝗿𝗮𝗯𝗲́𝗻𝘀!",
            ]
        )


@app.on_message(filters.command("love", prefixes="/"))
def love_command(client, message):
    command, *args = message.text.split(" ")
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()

        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        response = f"{name1}💕 + {name2}💕 = {love_percentage}%\n\n{love_message}"
    else:
        response = "⚠️ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗲𝗻𝘁𝗿𝗲 𝗱𝗼𝗶𝘀 𝗻𝗼𝗺𝗲𝘀 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /love."
    app.send_message(message.chat.id, response)


__MODULE__ = "💕𝗔𝗺𝗼𝗿"
__HELP__ = """
**🧡 𝗖𝗮𝗹𝗰𝘂𝗹𝗮𝗱𝗼𝗿 𝗱𝗲 𝗔𝗺𝗼𝗿:**

• `/love [nome1] [nome2]`: 💕 𝗖𝗮𝗹𝗰𝘂𝗹𝗮 𝗼 𝗽𝗲𝗿𝗰𝗲𝗻𝘁𝘂𝗮𝗹 𝗱𝗲 𝗮𝗺𝗼𝗿 𝗲𝗻𝘁𝗿𝗲 𝗱𝘂𝗮𝘀 𝗽𝗲𝘀𝘀𝗼𝗮𝘀.
"""
