import requests
from Cecilia import app
from pyrogram import filters

truth_api_url = "https://api.truthordarebot.xyz/v1/truth"
dare_api_url = "https://api.truthordarebot.xyz/v1/dare"


@app.on_message(filters.command("truth"))
def get_truth(client, message):
    try:
        response = requests.get(truth_api_url)
        if response.status_code == 200:
            truth_question = response.json()["question"]
            message.reply_text(f"💬 𝗣𝗲𝗿𝗴𝘂𝗻𝘁𝗮 𝗱𝗲 𝗩𝗲𝗿𝗱𝗮𝗱𝗲:\n\n{truth_question}")
        else:
            message.reply_text(
                "⚠️ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝘂𝗺𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮 𝗱𝗲 𝘃𝗲𝗿𝗱𝗮𝗱𝗲. 𝗧𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
            )
    except Exception as e:
        message.reply_text(
            "❌ 𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝘂𝗺𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮 𝗱𝗲 𝘃𝗲𝗿𝗱𝗮𝗱𝗲. 𝗧𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
        )


@app.on_message(filters.command("dare"))
def get_dare(client, message):
    try:
        response = requests.get(dare_api_url)
        if response.status_code == 200:
            dare_question = response.json()["question"]
            message.reply_text(f"🔥 𝗗𝗲𝘀𝗮𝗳𝗶𝗼:\n\n{dare_question}")
        else:
            message.reply_text(
                "⚠️ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝘂𝗺 𝗱𝗲𝘀𝗮𝗳𝗶𝗼. 𝗧𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
            )
    except Exception as e:
        message.reply_text(
            "❌ 𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝘂𝗺 𝗱𝗲𝘀𝗮𝗳𝗶𝗼. 𝗧𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
        )


__MODULE__ = "🔥𝗩𝗲𝗿𝗱𝗮𝗱𝗲"
__HELP__ = """
**📜 𝗖𝗢𝗠𝗔𝗡𝗗𝗢𝗦 𝗗𝗢 𝗕𝗢𝗧 𝗩𝗘𝗥𝗗𝗔𝗗𝗘 𝗢𝗨 𝗗𝗘𝗦𝗔𝗙𝗜𝗢**

𝗨𝘀𝗲 𝗼𝘀 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗮𝗯𝗮𝗶𝘅𝗼 𝗽𝗮𝗿𝗮 𝗷𝗼𝗴𝗮𝗿 𝗩𝗲𝗿𝗱𝗮𝗱𝗲 𝗼𝘂 𝗗𝗲𝘀𝗮𝗳𝗶𝗼:

- `/truth`: 🔎 𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝘂𝗺𝗮 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮 𝗱𝗲 𝘃𝗲𝗿𝗱𝗮𝗱𝗲. 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗵𝗼𝗻𝗲𝘀𝘁𝗮𝗺𝗲𝗻𝘁𝗲!
- `/dare`: 🔥 𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝘂𝗺 𝗱𝗲𝘀𝗮𝗳𝗶𝗼 𝗮𝘀𝘀𝘂𝘀𝘁𝗮𝗱𝗼𝗿. 𝗖𝘂𝗺𝗽𝗿𝗮 𝘀𝗲 𝗳𝗼𝗿 𝗰𝗼𝗿𝗮𝗷𝗼𝘀𝗼!

**📌 𝗘𝘅𝗲𝗺𝗽𝗹𝗼𝘀:**
- `/truth`: "𝗤𝘂𝗮𝗹 é 𝘀𝗲𝘂 𝗺𝗼𝗺𝗲𝗻𝘁𝗼 𝗺𝗮𝗶𝘀 𝗰𝗼𝗻𝘀𝘁𝗿𝗮𝗻𝗴𝗲𝗱𝗼?"
- `/dare`: "𝗙𝗮ç𝗮 𝟭𝟬 𝗳𝗹𝗲𝘅õ𝗲𝘀."

**⚠️ 𝗔𝗩𝗜𝗦𝗢:**
𝗦𝗲 𝘁𝗶𝘃𝗲𝗿 𝗽𝗿𝗼𝗯𝗹𝗲𝗺𝗮𝘀 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝗮𝘀 𝗽𝗲𝗿𝗴𝘂𝗻𝘁𝗮𝘀, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲.
"""
