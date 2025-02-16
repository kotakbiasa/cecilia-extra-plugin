import requests
from Cecilia import app
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@app.on_message(
    filters.command(
        [
            "dice",
            "ludo",
            "dart",
            "basket",
            "basketball",
            "football",
            "slot",
            "bowling",
            "jackpot",
        ]
    )
)
async def dice(client: Client, message: Message):
    command = message.text.split()[0]
    if command == "/dice" or command == "/ludo":
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔄", callback_data="send_dice")]]
        )
        value = await client.send_dice(message.chat.id, reply_markup=keyboard)

    elif command == "/dart":
        value = await client.send_dice(message.chat.id, emoji="🎯", reply_to_message_id=message.id)
        await value.reply_text("𝗦𝘂𝗮 𝗽𝗼𝗻𝘁𝘂𝗮𝗰̧𝗮̃𝗼 𝗲́: {0}".format(value.dice.value))

    elif command == "/basket" or command == "/basketball":
        basket = await client.send_dice(message.chat.id, emoji="🏀", reply_to_message_id=message.id)
        await basket.reply_text("𝗦𝘂𝗮 𝗽𝗼𝗻𝘁𝘂𝗮𝗰̧𝗮̃𝗼 𝗲́: {0}".format(basket.dice.value))

    elif command == "/football":
        value = await client.send_dice(message.chat.id, emoji="⚽", reply_to_message_id=message.id)
        await value.reply_text("𝗦𝘂𝗮 𝗽𝗼𝗻𝘁𝘂𝗮𝗰̧𝗮̃𝗼 𝗲́: {0}".format(value.dice.value))

    elif command == "/slot" or command == "/jackpot":
        value = await client.send_dice(message.chat.id, emoji="🎰", reply_to_message_id=message.id)
        await value.reply_text("𝗦𝘂𝗮 𝗽𝗼𝗻𝘁𝘂𝗮𝗰̧𝗮̃𝗼 𝗲́: {0}".format(value.dice.value))

    elif command == "/bowling":
        value = await client.send_dice(message.chat.id, emoji="🎳", reply_to_message_id=message.id)
        await value.reply_text("𝗦𝘂𝗮 𝗽𝗼𝗻𝘁𝘂𝗮𝗰̧𝗮̃𝗼 𝗲́: {0}".format(value.dice.value))


bored_api_url = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command("bored", prefixes="/"))
async def bored_command(_client: Client, message):
    response = requests.get(bored_api_url)
    if response.status_code == 200:
        data = response.json()
        activity = data.get("activity")
        if activity:
            await message.reply(f"🌀 **𝗘𝘀𝘁𝗮́ 𝗲𝗻𝘁𝗲𝗱𝗶𝗮𝗱𝗼? 𝗤𝘂𝗲 𝘁𝗮𝗹:**\n\n{activity}")
        else:
            await message.reply("⚠️ **𝗡𝗲𝗻𝗵𝘂𝗺𝗮 𝗮𝘁𝗶𝘃𝗶𝗱𝗮𝗱𝗲 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗱𝗮.**")
    else:
        await message.reply("❌ **𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗿𝗲𝗰𝘂𝗽𝗲𝗿𝗮𝗿 𝘂𝗺𝗮 𝗮𝘁𝗶𝘃𝗶𝗱𝗮𝗱𝗲.**")


@app.on_callback_query(filters.regex(r"send_dice"))
async def dice_again(client: Client, callback_query: CallbackQuery):
    try:
        await app.edit_message_text(
            callback_query.message.chat.id, callback_query.message.id, callback_query.message.dice.emoji
        )
    except BaseException:
        pass
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄", callback_data="send_dice")]]
    )
    await client.send_dice(callback_query.message.chat.id, reply_markup=keyboard)


__MODULE__ = "🎉 𝗙𝘂𝗻"
__HELP__ = """
**𝗣𝗮𝗿𝗮 𝗱𝗶𝘃𝗲𝗿𝘀𝗮̃𝗼:**

• `/dice`: 🎲 **𝗥𝗼𝗱𝗮 𝘂𝗺 𝗱𝗮𝗱𝗼.**
• `/ludo`: 🎲 **𝗝𝗼𝗴𝗮 𝗟𝘂𝗱𝗼.**
• `/dart`: 🎯 **𝗟𝗮𝗻𝗰̧𝗮 𝘂𝗺 𝗱𝗮𝗿𝘁.**
• `/basket` ou `/basketball`: 🏀 **𝗝𝗼𝗴𝗮 𝗕𝗮𝘀𝗾𝘂𝗲𝘁𝗲.**
• `/football`: ⚽ **𝗝𝗼𝗴𝗮 𝗙𝘂𝘁𝗲𝗯𝗼𝗹.**
• `/slot` ou `/jackpot`: 🎰 **𝗝𝗼𝗴𝗮 𝗝𝗮𝗰𝗸𝗽𝗼𝘁.**
• `/bowling`: 🎳 **𝗝𝗼𝗴𝗮 𝗕𝗼𝗹𝗶𝗻𝗵𝗮.**
• `/bored`: 🌀 **𝗥𝗲𝗰𝗲𝗯𝗲 𝘂𝗺𝗮 𝗮𝘁𝗶𝘃𝗶𝗱𝗮𝗱𝗲 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗮 𝘀𝗲 𝗲𝘀𝘁𝗶𝘃𝗲𝗿 𝗲𝗻𝘁𝗲𝗱𝗶𝗮𝗱𝗼.**
"""
