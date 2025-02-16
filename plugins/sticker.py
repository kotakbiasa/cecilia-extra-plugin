import imghdr
import math
import os
from asyncio import gather
from traceback import format_exc
from typing import List

from PIL import Image
from Cecilia import app
from pyrogram import Client, errors, filters, raw
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from utils.error import capture_err

BOT_USERNAME = app.username

MAX_STICKERS = (
    120  # would be better if we could fetch this limit directly from telegram
)
SUPPORTED_TYPES = ["jpeg", "png", "webp"]
STICKER_DIMENSIONS = (512, 512)


async def get_sticker_set_by_name(
        client: Client, name: str
) -> raw.base.messages.StickerSet:
    try:
        return await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=name),
                hash=0,
            )
        )
    except errors.exceptions.not_acceptable_406.StickersetInvalid:
        return None


async def create_sticker_set(
        client: Client,
        owner: int,
        title: str,
        short_name: str,
        stickers: List[raw.base.InputStickerSetItem],
) -> raw.base.messages.StickerSet:
    return await client.invoke(
        raw.functions.stickers.CreateStickerSet(
            user_id=await client.resolve_peer(owner),
            title=title,
            short_name=short_name,
            stickers=stickers,
        )
    )


async def add_sticker_to_set(
        client: Client,
        stickerset: raw.base.messages.StickerSet,
        sticker: raw.base.InputStickerSetItem,
) -> raw.base.messages.StickerSet:
    return await client.invoke(
        raw.functions.stickers.AddStickerToSet(
            stickerset=raw.types.InputStickerSetShortName(
                short_name=stickerset.set.short_name
            ),
            sticker=sticker,
        )
    )


async def create_sticker(
        sticker: raw.base.InputDocument, emoji: str
) -> raw.base.InputStickerSetItem:
    return raw.types.InputStickerSetItem(document=sticker, emoji=emoji)


async def resize_file_to_sticker_size(file_path: str) -> str:
    im = Image.open(file_path)
    if (im.width, im.height) < STICKER_DIMENSIONS:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = STICKER_DIMENSIONS[0] / size1
            size1new = STICKER_DIMENSIONS[0]
            size2new = size2 * scale
        else:
            scale = STICKER_DIMENSIONS[1] / size2
            size1new = size1 * scale
            size2new = STICKER_DIMENSIONS[1]
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(STICKER_DIMENSIONS)
    try:
        os.remove(file_path)
        file_path = f"{file_path}.png"
        return file_path
    finally:
        im.save(file_path)


async def upload_document(
        client: Client, file_path: str, chat_id: int
) -> raw.base.InputDocument:
    media = await client.invoke(
        raw.functions.messages.UploadMedia(
            peer=await client.resolve_peer(chat_id),
            media=raw.types.InputMediaUploadedDocument(
                mime_type=client.guess_mime_type(file_path) or "application/zip",
                file=await client.save_file(file_path),
                attributes=[
                    raw.types.DocumentAttributeFilename(
                        file_name=os.path.basename(file_path)
                    )
                ],
            ),
        )
    )
    return raw.types.InputDocument(
        id=media.document.id,
        access_hash=media.document.access_hash,
        file_reference=media.document.file_reference,
    )


async def get_document_from_file_id(
        file_id: str,
) -> raw.base.InputDocument:
    decoded = FileId.decode(file_id)
    return raw.types.InputDocument(
        id=decoded.media_id,
        access_hash=decoded.access_hash,
        file_reference=decoded.file_reference,
    )


@app.on_message(filters.command("stickerid"))
@capture_err
async def sticker_id(_, message: Message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply("𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿. ✋")

    if not reply.sticker:
        return await message.reply("𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿. 🖼️")

    await message.reply_text(f"`{reply.sticker.file_id}`")


@app.on_message(filters.command("getsticker"))
@capture_err
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r:
        return await message.reply("𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿. ✋")

    if not r.sticker:
        return await message.reply("𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿. 🖼️")

    m = await message.reply("𝗘𝗻𝘃𝗶𝗮𝗻𝗱𝗼... ⏳")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )

    await m.delete()
    os.remove(f)


@app.on_message(filters.command("kang"))
@capture_err
async def kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿/𝗶𝗺𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗸𝗮𝗻𝗴𝗮𝗿. 🖼️✨")
    if not message.from_user:
        return await message.reply_text(
            "𝗩𝗼𝗰𝗲̂ 𝗲́ 𝘂𝗺 𝗮𝗱𝗺𝗶𝗻 𝗮𝗻ô𝗻𝗶𝗺𝗼, 𝗸𝗮𝗻𝗴𝗮𝗿 𝘀𝘁𝗶𝗰𝗸𝗲𝗿𝘀 𝗻𝗼𝘀 𝗺𝗲𝘂𝘀 𝗣𝗠. 🛡️")
    msg = await message.reply_text("𝗞𝗮𝗻𝗴𝗮𝗻𝗱𝗼 𝗦𝘁𝗶𝗰𝗸𝗲𝗿... 🛠️")

    # Find the proper emoji
    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif message.reply_to_message.sticker and message.reply_to_message.sticker.emoji:
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "🤔"

    # Get the corresponding fileid, resize the file if necessary
    doc = message.reply_to_message.photo or message.reply_to_message.document
    try:
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(
                    message.reply_to_message.sticker.file_id
                ),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10000000:
                return await msg.edit("𝗔𝗿𝗾𝘂𝗶𝘃𝗼 𝗺𝘂𝗶𝘁𝗼 𝗴𝗿𝗮𝗻𝗱𝗲. 🚫")

            temp_file_path = await app.download_media(doc)
            image_type = imghdr.what(temp_file_path)
            if image_type not in SUPPORTED_TYPES:
                return await msg.edit("𝗙𝗼𝗿𝗺𝗮𝘁𝗼 𝗻𝗮̃𝗼 𝘀𝘂𝗽𝗼𝗿𝘁𝗮𝗱𝗼! ({}) ❌".format(image_type))
            try:
                temp_file_path = await resize_file_to_sticker_size(temp_file_path)
            except OSError as e:
                await msg.edit_text("𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗮𝗱𝗼. ⚠️")
                raise Exception(
                    f"Algo deu errado ao redimensionar o sticker (em {temp_file_path}); {e}"
                )
            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        else:
            return await msg.edit("𝗡𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗸𝗮𝗻𝗴𝗮𝗿 𝗶𝘀𝘀𝗼. ❌")
    except ShortnameOccupyFailed:
        await message.reply_text("𝗠𝘂𝗱𝗲 𝘀𝗲𝘂 𝗻𝗼𝗺𝗲 𝗼𝘂 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂á𝗿𝗶𝗼. 🛑")
        return

    except Exception as e:
        await message.reply_text(str(e))
        e = format_exc()
        return print(e)

    # Find an available pack & add the sticker to the pack; create a new pack if needed
    # Would be a good idea to cache the number instead of searching it every
    # single time...
    packnum = 0
    packname = "f" + str(message.from_user.id) + "_by_" + BOT_USERNAME
    limit = 0
    try:
        while True:
            # Prevent infinite rules
            if limit >= 50:
                return await msg.delete()

            stickerset = await get_sticker_set_by_name(client, packname)
            if not stickerset:
                stickerset = await create_sticker_set(
                    client,
                    message.from_user.id,
                    f"{message.from_user.first_name[:32]}'s kang pack",
                    packname,
                    [sticker],
                )
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = (
                        "f"
                        + str(packnum)
                        + "_"
                        + str(message.from_user.id)
                        + "_by_"
                        + BOT_USERNAME
                )
                limit += 1
                continue
            else:
                try:
                    await add_sticker_to_set(client, stickerset, sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("[𝗘𝗥𝗥𝗢]: 𝗘𝗠𝗢𝗝𝗜_𝗜𝗡𝗩Á𝗟𝗜𝗗𝗢 𝗡𝗔 𝗔𝗥𝗚𝗨𝗠𝗘𝗡𝗧𝗔𝗖̧Ã𝗢 ❌")
            limit += 1
            break

        await msg.edit(
            "𝗦𝘁𝗶𝗰𝗸𝗲𝗿 𝗸𝗮𝗻𝗴𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 [𝗣𝗮𝗰𝗸](t.me/addstickers/{})\n𝗘𝗺𝗼𝗷𝗶: {} 🎨".format(
                packname, sticker_emoji
            )
        )
    except (PeerIdInvalid, UserIsBlocked):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="𝗜𝗻𝗶𝗰𝗶𝗮𝗿", url=f"t.me/{BOT_USERNAME}")]]
        )
        await msg.edit(
            "𝗩𝗼𝗰𝗲̂ 𝗽𝗿𝗲𝗰𝗶𝘀𝗮 𝗶𝗻𝗶𝗰𝗶𝗮𝗿 𝘂𝗺 𝗰𝗵𝗮𝘁 𝗽𝗿𝗶𝘃𝗮𝗱𝗼 𝗰𝗼𝗺𝗶𝗴𝗼. 📩",
            reply_markup=keyboard,
        )
    except StickerPngNopng:
        await message.reply_text(
            "𝗢𝘀 𝘀𝘁𝗶𝗰𝗸𝗲𝗿𝘀 𝗽𝗿𝗲𝗰𝗶𝘀𝗮𝗺 𝘀𝗲𝗿 𝗮𝗿𝗾𝘂𝗶𝘃𝗼𝘀 𝗲𝗺 𝗽𝗻𝗴, 𝗺𝗮𝘀 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗽𝗿𝗼𝘃𝗶𝗱𝗮 𝗻ã𝗼 𝗲𝗿𝗮 𝗽𝗻𝗴. 🖼️🚫"
        )
    except StickerPngDimensions:
        await message.reply_text("𝗔𝘀 𝗱𝗶𝗺𝗲𝗻𝘀𝗼̃𝗲𝘀 𝗱𝗼 𝗽𝗻𝗴 𝗱𝗼 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝘀ã𝗼 𝗶𝗻𝘃á𝗹𝗶𝗱𝗮𝘀. 📏❌")


__MODULE__ = "🖼𝗦𝘁𝗶𝗰𝗸𝗲𝗿𝘀"
__HELP__ = """
**𝗖𝗢𝗠𝗔𝗡𝗗𝗢𝗦:**

• /stickerid - **𝗢𝗯𝘁é𝗺 𝗼 𝗶𝗱 𝗱𝗼 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗱𝗲 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗿𝗲𝗽𝗹𝗶𝗰𝗮𝗱𝗼.**
• /getsticker - **𝗢𝗯𝘁é𝗺 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗲 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗿𝗲𝗽𝗹𝗶𝗰𝗮𝗱𝗼.**
• /kang - **𝗞𝗮𝗻𝗴𝗮 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗻𝗼 𝘀𝗲𝘂 𝗽𝗮𝗰𝗸.**

**𝗜𝗡𝗙𝗢:**

- 𝗘𝘀𝘀𝗲 𝗯𝗼𝘁 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗮𝗼𝘀 𝘂𝘀𝘂á𝗿𝗶𝗼𝘀 𝗼𝗯𝘁𝗲𝗿 𝗼 𝗶𝗱 𝗱𝗼 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗼𝘂 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗲 𝘂𝗺 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗿𝗲𝗽𝗹𝗶𝗰𝗮𝗱𝗼 𝗲 𝘁𝗮𝗺𝗯é𝗺 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗸𝗮𝗻𝗴𝗮𝗿 𝗲 𝗮𝗱𝗶𝗰𝗶𝗼𝗻á-𝗹𝗼 𝗮 𝘂𝗺 𝗽𝗮𝗰𝗼𝘁𝗲 𝗱𝗲 𝘀𝘁𝗶𝗰𝗸𝗲𝗿.
"""
