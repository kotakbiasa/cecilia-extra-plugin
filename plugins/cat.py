import requests
from Cecilia import app
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
        [InlineKeyboardButton(text="🔄 **𝗔𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗿**", callback_data="refresh_cat")],
        [InlineKeyboardButton(text="❌ **𝗙𝗲𝗰𝗵𝗮𝗿**", callback_data="close")],
    ]
)


@app.on_message(filters.command("cat") & ~BANNED_USERS)
async def cat(_client: Client, message: Message):
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            await message.reply_animation(
                cat_url, caption="🐱 **𝗠𝗲𝗼𝘄**", reply_markup=close_keyboard
            )
        else:
            await message.reply_photo(cat_url, caption="🐱 **𝗠𝗲𝗼𝘄**", reply_markup=close_keyboard)
    else:
        await message.reply_text("🙀 **𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗯𝘂𝘀𝗰𝗮𝗿 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗴𝗮𝘁𝗼!**")


@app.on_callback_query(filters.regex("refresh_cat") & ~BANNED_USERS)
async def refresh_cat(_client: Client, callback_query: CallbackQuery):
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            await callback_query.edit_message_animation(
                cat_url, caption="🐱 **𝗠𝗲𝗼𝘄**", reply_markup=close_keyboard
            )
        else:
            await callback_query.edit_message_media(
                InputMediaPhoto(media=cat_url, caption="🐱 **𝗠𝗲𝗼𝘄**"),
                reply_markup=close_keyboard,
            )
    else:
        await callback_query.edit_message_text("🙀 **𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗮𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗿 𝗮 𝗳𝗼𝘁𝗼 𝗱𝗼 𝗴𝗮𝘁𝗼!**")
