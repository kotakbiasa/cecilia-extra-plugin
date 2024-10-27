import requests
from WinxMusic import app
from config import BANNED_USERS
from pyrogram import filters, Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)

close_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="🔄 **𝗔𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗿**", callback_data="refresh_dog")],
        [InlineKeyboardButton(text="❌ **𝗙𝗲𝗰𝗵𝗮𝗿**", callback_data="close")],
    ]
)


@app.on_message(filters.command(["dogs", "dog"]) & ~BANNED_USERS)
async def dog(_client: Client, message: Message):
    r = requests.get("https://random.dog/woof.json")
    if r.status_code == 200:
        data = r.json()
        dog_url = data["url"]
        if dog_url.endswith(".gif"):
            await message.reply_animation(dog_url, reply_markup=close_keyboard)
        else:
            await message.reply_photo(dog_url, reply_markup=close_keyboard)
    else:
        await message.reply_text("🐕 **𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗯𝘂𝘀𝗰𝗮𝗿 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗰𝗮𝗰𝗵𝗼𝗿𝗿𝗼!**")


@app.on_callback_query(filters.regex("refresh_dog") & ~BANNED_USERS)
async def refresh_dog(_client: Client, callback_query: CallbackQuery):
    r = requests.get("https://random.dog/woof.json")
    if r.status_code == 200:
        data = r.json()
        dog_url = data["url"]
        if dog_url.endswith(".gif"):
            await callback_query.edit_message_animation(dog_url, reply_markup=close_keyboard)
        else:
            await callback_query.edit_message_media(
                InputMediaPhoto(media=dog_url),
                reply_markup=close_keyboard,
            )
    else:
        await callback_query.edit_message_text(
            "🐕 **𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗮𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗿 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗰𝗮𝗰𝗵𝗼𝗿𝗿𝗼!**")
