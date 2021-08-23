# (c) @AbirHasan2005

import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, MessageNotModified


async def SendMessage(bot: Client, text, updates_channel_id):
    try:
        sent_message = await bot.send_message(
            chat_id=updates_channel_id,
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return sent_message
    except FloodWait as e:
        print(f"Sleep of {e.x} required by FloodWait ...")
        await asyncio.sleep(e.x)
        return SendMessage(bot, text, updates_channel_id)


async def EditMessage(editable: Message, text):
    try:
        await editable.edit(
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    except FloodWait as e:
        print(f"Sleep of {e.x} required by FloodWait ...")
        await asyncio.sleep(e.x)
        await EditMessage(editable, text)
    except MessageNotModified:
        pass
