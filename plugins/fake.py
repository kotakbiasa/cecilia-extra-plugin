import requests
from WinxMusic import app
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command(["FAKE", "fake"]))
async def fk_address(_, message: Message):
    query = message.text.split(maxsplit=1)[1].strip()
    url = f"https://randomuser.me/api/?nat={query}"
    response = requests.get(url)
    data = response.json()

    if "results" in data:
        fk = data["results"][0]

        name = f"{fk['name']['title']} {fk['name']['first']} {fk['name']['last']}"
        address = (
            f"{fk['location']['street']['number']} {fk['location']['street']['name']}"
        )
        city = fk["location"]["city"]
        state = fk["location"]["state"]
        country = fk["location"]["country"]
        postal = fk["location"]["postcode"]
        email = fk["email"]
        phone = fk["phone"]
        picture = fk["picture"]["large"]
        gender = fk["gender"]

        fkinfo = f"""
**👤 𝗡𝗼𝗺𝗲:** `{name}`
**⚧️ 𝗚𝗲̂𝗻𝗲𝗿𝗼:** `{gender}`
**🏠 𝗘𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼:** `{address}`
**🌎 𝗣𝗮𝗶́𝘀:** `{country}`
**🏙️ 𝗖𝗶𝗱𝗮𝗱𝗲:** `{city}`
**🌐 𝗘𝘀𝘁𝗮𝗱𝗼:** `{state}`
**📮 𝗖𝗘𝗣:** `{postal}`
**📧 𝗘𝗺𝗮𝗶𝗹:** `{email}`
**📞 𝗧𝗲𝗹𝗲𝗳𝗼𝗻𝗲:** `{phone}`
        """

        await message.reply_photo(photo=picture, caption=fkinfo)
    else:
        await message.reply_text(
            "❌ **𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗱𝗼 𝗻𝗲𝗻𝗵𝘂𝗺 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼. 𝗧𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲!**")


__MODULE__ = "📄 𝗙𝗮𝗸𝗲"
__HELP__ = """
/fake [𝗰𝗼́𝗱𝗶𝗴𝗼 𝗱𝗼 𝗽𝗮𝗶́𝘀] - **𝗣𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝘂𝗺 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗼**
"""
