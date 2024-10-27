"""from os import remove
from pyrogram import filters
from lexica import Client as LexicaClient
from pyrogram.errors.exceptions.bad_request_400 import PhotoInvalidDimensions
from WinxMusic import app
from utils.error import capture_err

lexica_client = LexicaClient()

def upscale_image(image: bytes) -> bytes:
    return lexica_client.upscale(image)

@app.on_message(filters.command("upscale"))
@capture_err
async def upscale_reply_image(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text("𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗽𝗮𝗿𝗮 𝗳𝗮𝘇𝗲𝗿 𝘂𝗽𝘀𝗰𝗮𝗹𝗲 𝗻𝗲𝗹𝗮...😑")
    if message.reply_to_message.photo:
        a = await message.reply_text("𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲 𝘂𝗺 𝗺𝗼𝗺𝗲𝗻𝘁𝗼...⏳")
        photo = await client.download_media(message.reply_to_message.photo.file_id)

        with open(photo, 'rb') as f:
            image_bytes = f.read()
        try:
            upscaled_image_bytes = upscale_image(image_bytes)
            await a.edit("𝗤𝘂𝗮𝘀𝗲 𝗽𝗿𝗼𝗻𝘁𝗼...❣️")
            with open('upscaled.png', 'wb') as f:
                f.write(upscaled_image_bytes)
                try:
                    await message.reply_photo(photo='upscaled.png')
                    remove('upscaled.png')
                    await a.delete()
                except PhotoInvalidDimensions:
                    await message.reply_document('upscaled.png')
                    remove('upscaled.png')
                    await a.delete()
        except Exception as e:
            remove('upscaled.png')
            await a.edit(f"𝗘𝗿𝗿𝗼: {e} ❗")"""
