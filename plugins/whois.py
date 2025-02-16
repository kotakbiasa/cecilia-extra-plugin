from Cecilia import app
from pyrogram import filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message, User


def reply_check(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


infotext = (
    "[{full_name}](tg://user?id={user_id})\n\n"
    " ➻ 𝗨𝘀𝗲𝗿 𝗜𝗗: `{user_id}`\n"
    " ➻ 𝗣𝗿𝗶𝗺𝗲𝗶𝗿𝗼 𝗡𝗼𝗺𝗲: `{first_name}`\n"
    " ➻ 𝗨́𝗹𝘁𝗶𝗺𝗼 𝗡𝗼𝗺𝗲: `{last_name}`\n"
    " ➻ 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: `@{username}`\n"
    " ➻ 𝗨́𝗹𝘁𝗶𝗺𝗮 𝘃𝗲𝘇 𝗼𝗻𝗹𝗶𝗻𝗲: `{last_online}`"
)


def last_online(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "𝗿𝗲𝗰𝗲𝗻𝘁𝗲𝗺𝗲𝗻𝘁𝗲"
    elif user.status == "within_week":
        return "𝗻𝗼 𝘂́𝗹𝘁𝗶𝗺𝗼 𝘀𝗲𝗺𝗮𝗻𝗮"
    elif user.status == "within_month":
        return "𝗻𝗼 𝘂́𝗹𝘁𝗶𝗺𝗼 𝗺𝗲̂𝘀"
    elif user.status == "long_time_ago":
        return "𝗵𝗮́ 𝗺𝘂𝗶𝘁𝗼 𝘁𝗲𝗺𝗽𝗼 :("
    elif user.status == "online":
        return "𝗮𝗰𝘁𝘂𝗮𝗹𝗺𝗲𝗻𝘁𝗲 𝗼𝗻𝗹𝗶𝗻𝗲"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.status.date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


def full_name(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@app.on_message(filters.command("whois"))
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("Não conheço este usuário.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    await message.reply_text(
        infotext.format(
            full_name=full_name(user),
            user_id=user.id,
            user_dc=user.dc_id,
            first_name=user.first_name,
            last_name=user.last_name if user.last_name else "",
            username=user.username if user.username else "",
            last_online=last_online(user),
            bio=desc if desc else "𝗩𝗮𝘇𝗶𝗼.",
        ),
        disable_web_page_preview=True,
    )


__MODULE__ = "🆔 𝗜𝗻𝗳𝗼"
__HELP__ = """
**Comando:**

• /whois - **𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗮̃𝗼 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.**

**𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀:**

- 𝗘𝘀𝘁𝗲 𝗯𝗼𝘁 𝗽𝗿𝗼𝘃𝗶𝗱𝗲𝗻𝗰𝗶𝗮 𝘂𝗺 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝘃𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗮̃𝗼 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.
- 𝗨𝘀𝗲 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /whois 𝘀𝗲𝗴𝘂𝗶𝗱𝗼 𝗽𝗼𝗿 𝘂𝗺𝗮 𝗿𝗲𝘀𝗽𝗼𝘀𝘁𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗼𝘂 𝗨𝘀𝗲𝗿 𝗜𝗗 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗮̃𝗼 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.

**𝗡𝗼𝘁𝗮:**

- 𝗢 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /whois 𝗽𝗼𝗱𝗲 𝘀𝗲𝗿 𝘂𝘀𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 𝗿𝗲𝘁𝗿𝗶𝗯𝘂𝗶𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗻𝗼 𝗰𝗵𝗮𝘁.
- 𝗔𝘀 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗶𝗻𝗰𝗹𝘂𝗶𝗺 𝗜𝗗, 𝗣𝗿𝗶𝗺𝗲𝗶𝗿𝗼 𝗡𝗼𝗺𝗲, 𝗨́𝗹𝘁𝗶𝗺𝗼 𝗡𝗼𝗺𝗲, 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗲 𝘀𝘁𝗮𝘁𝘂𝘀 𝗼𝗻𝗹𝗶𝗻𝗲.
"""
