import requests
from WinxMusic import app
from pyrogram import filters
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def download_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return (
                f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗯𝗮𝗶𝘅𝗮𝗿 𝗼 𝗰𝗼́𝗱𝗶𝗴𝗼-𝗳𝗼𝗻𝘁𝗲. 𝗖𝗼́𝗱𝗶𝗴𝗼 𝗱𝗲 𝗲𝘀𝘁𝗮𝗱𝗼: {response.status_code} 🚫"
            )

    except Exception as e:
        return f"𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼𝗿: {str(e)} ⚠️"


# Handler para o comando /webdl para baixar o código-fonte do site
@app.on_message(filters.command("webdl"))
def web_download(client, message):
    # Verifica se o comando possui uma URL anexada
    if len(message.command) == 1:
        message.reply_text(
            "❌ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗲𝗻𝘁𝗿𝗲 𝗰𝗼𝗺 𝘂𝗺𝗮 𝗨𝗥𝗟 𝗷𝘂𝗻𝘁𝗼 𝗰𝗼𝗺 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /webdl.")
        return

    # Obtém a URL após o comando /webdl
    url = message.command[1]

    source_code = download_website(url)
    if source_code.startswith("𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼𝗿") or source_code.startswith(
            "𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗯𝗮𝗶𝘅𝗮𝗿"
    ):
        message.reply_text(source_code)
    else:
        with open("website.txt", "w", encoding="utf-8") as file:
            file.write(source_code)
        message.reply_document(document="website.txt", caption=f"📄 𝗖𝗼́𝗱𝗶𝗴𝗼-𝗳𝗼𝗻𝘁𝗲 𝗱𝗲 {url}")


__MODULE__ = "🔗𝗦𝗶𝘁𝗲"
__HELP__ = """
**🛠 𝗖𝗢𝗠𝗔𝗡𝗗𝗢:**

• /webdl - **𝗕𝗮𝗶𝘅𝗮𝗿 𝗼 𝗰𝗼́𝗱𝗶𝗴𝗼-𝗳𝗼𝗻𝘁𝗲 𝗱𝗼 𝘀𝗶𝘁𝗲.**

**ℹ️ 𝗜𝗡𝗙𝗢:**

- 𝗘𝘀𝘁𝗲 𝗯𝗼𝘁 𝗽𝗿𝗼𝘃𝗶𝗱𝗲𝗻𝗰𝗶𝗮 𝘂𝗺 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝗯𝗮𝗶𝘅𝗮𝗿 𝗼 𝗰𝗼́𝗱𝗶𝗴𝗼-𝗳𝗼𝗻𝘁𝗲 𝗱𝗲 𝘂𝗺 𝘀𝗶𝘁𝗲.
- 𝗨𝘀𝗲 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /webdl 𝗰𝗼𝗺 𝘂𝗺𝗮 𝗨𝗥𝗟 𝗽𝗮𝗿𝗮 𝗯𝗮𝗶𝘅𝗮𝗿 𝗼 𝗰𝗼́𝗱𝗶𝗴𝗼-𝗳𝗼𝗻𝘁𝗲 𝗱𝗼 𝘀𝗶𝘁𝗲.

**🔔 𝗡𝗢𝗧𝗔:**

- 𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗼𝗱𝗲 𝘀𝗲𝗿 𝘂𝘀𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 𝗯𝗮𝗶𝘅𝗮𝗿 𝗼 𝗰𝗼́𝗱𝗶𝗴𝗼-𝗳𝗼𝗻𝘁𝗲 𝗱𝗲 𝘀𝗶𝘁𝗲𝘀.
- 𝗢 𝗰𝗼́𝗱𝗶𝗴𝗼-𝗳𝗼𝗻𝘁𝗲 𝘀𝗲𝗿𝗮́ 𝗲𝗻𝘃𝗶𝗮𝗱𝗼 𝗲𝗺 𝗳𝗼𝗿𝗺𝗮 𝗱𝗲 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗻𝗮 𝗰𝗼𝗻𝘃𝗲𝗿𝘀𝗮. 📩
"""
