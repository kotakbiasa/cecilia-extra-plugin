import asyncio
import logging

from Cecilia import app
from Cecilia.utils.database import (
    get_assistant,
)
from config import BANNED_USERS
from pyrogram import filters, Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    UserNotParticipant,
)
from pyrogram.types import Message

RADIO_STATION = {
    "Air Bilaspur": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio110/playlist.m3u8",
    "Air Raipur": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio118/playlist.m3u8",
    "Capital FM": "http://media-ice.musicradio.com/CapitalMP3?.mp3&listening-from-radio-garden=1616312105154",
    "English": "https://hls-01-regions.emgsound.ru/11_msk/playlist.m3u8",
    "Mirchi": "http://peridot.streamguys.com:7150/Mirchi",
    "Radio Today": "http://stream.zenolive.com/8wv4d8g4344tv",
    "Retro Bollywood": "https://stream.zeno.fm/g372rxef798uv",
    "Hits Of Bollywood": "https://stream.zeno.fm/60ef4p33vxquv",
    "Dhol Radio": "https://radio.dholradio.co:8000/radio.mp3",
    "City 91.1 FM": "https://prclive1.listenon.in/",
    "Radio Udaan": "http://173.212.234.220/radio/8000/radio.mp3",
    "All India Radio Patna": "https://air.pc.cdn.bitgravity.com/air/live/pbaudio087/playlist.m3u8",
    "Mirchi 98.3 FM": "https://playerservices.streamtheworld.com/api/livestream-redirect/NJS_HIN_ESTAAC.m3u8",
    "Hungama 90s Once Again": "https://stream.zeno.fm/rm4i9pdex3cuv",
    "Hungama Evergreen Bollywood": "https://server.mixify.in:8010/radio.mp3"
}

valid_stations = "\n".join([f"`{name}`" for name in sorted(RADIO_STATION.keys())])


@app.on_message(
    filters.command(["radioplayforce", "radio", "cradio"])
    & filters.group
    & ~BANNED_USERS
)
async def radio(client: Client, message: Message):
    msg = await message.reply_text("𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲 𝘂𝗺 𝗺𝗼𝗺𝗲𝗻𝘁𝗼... ⏳")
    try:
        try:
            userbot = await get_assistant(message.chat.id)
            get = await app.get_chat_member(message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await msg.edit_text(
                f"❗ 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗻𝗲𝗰𝗲𝘀𝘀𝗮́𝗿𝗶𝗮 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗮 𝗼 𝗴𝗿𝘂𝗽𝗼 {message.chat.title}.",
            )
        if get.status == ChatMemberStatus.BANNED:
            return await msg.edit_text(
                text=f"⚠️ 𝗢 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗲𝘀𝘁𝗮́ 𝗯𝗹𝗼𝗾𝘂𝗲𝗮𝗱𝗼 𝗲𝗺 {message.chat.title}\n\n𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗱𝗲𝘀𝗯𝗹𝗼𝗾𝘂𝗲𝗶𝗲 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗮𝗿..."
            )
    except UserNotParticipant:
        if message.chat.username:
            invitelink = message.chat.username
            try:
                await userbot.resolve_peer(invitelink)
            except Exception as ex:
                logging.exception(ex)
        else:
            try:
                invitelink = await client.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await msg.edit_text(
                    f"❗ 𝗡𝗮̃𝗼 𝗵𝗮́ 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝗼 𝗴𝗿𝘂𝗽𝗼 {message.chat.title}."
                )
            except Exception as ex:
                return await msg.edit_text(
                    f"𝗘𝗿𝗿𝗼𝗿: 𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼: `{ex}`"
                )
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        anon = await msg.edit_text(
            f"🔄 𝗖𝗼𝗻𝘃𝗶𝗱𝗮𝗻𝗱𝗼 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}..."
        )
        try:
            await userbot.join_chat(invitelink)
            await asyncio.sleep(2)
            await msg.edit_text(
                f"🎉 {userbot.mention} 𝗲𝗻𝘁𝗿𝗼𝘂 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼, 𝗶𝗻𝗶𝗰𝗶𝗮𝗻𝗱𝗼 𝗮 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼..."
            )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                return await msg.edit_text(
                    f"⚠️ 𝗦𝗲𝗺 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}."
                )
            else:
                return await msg.edit_text(
                    f"𝗘𝗿𝗿𝗼𝗿 𝗻𝗮 𝗰𝗼𝗻𝘃𝗶𝘁𝗮𝗰̧𝗮̃𝗼: `{ex}`"
                )

    await msg.delete()
    station_name = " ".join(message.command[1:])
    RADIO_URL = RADIO_STATION.get(station_name)
    if RADIO_URL:
        await message.reply_text(
            f"📻 𝗣𝗹𝗮𝘆𝗶𝗻𝗴: `{station_name}`"
        )
    else:
        await message.reply(
            f"🎶 𝗣𝗮𝗿𝗮 𝗲𝘀𝗰𝘂𝘁𝗮𝗿, 𝗲𝘀𝗰𝗼𝗹𝗵𝗮 𝘂𝗺𝗮 𝗲𝘀𝘁𝗮𝗰̧𝗮̃𝗼 𝗱𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗹:\n{valid_stations}"
        )


__MODULE__ = "📻𝗥𝗮́𝗱𝗶𝗼"
__HELP__ = f"\n/radio [𝗲𝘀𝘁𝗮𝗰̧𝗮̃𝗼] - 𝗧𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗲 𝗿𝗮́𝗱𝗶𝗼 𝗻𝗼 𝗴𝗿𝘂𝗽𝗼! 📻\n𝗘𝘀𝘁𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗶𝘀:\n{valid_stations}"
