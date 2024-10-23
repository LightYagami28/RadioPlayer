"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from config import Config, STREAM
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME
from pyrogram import Client, filters, emoji

# Configuration variables
ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
LOG_GROUP = Config.LOG_GROUP

async def is_admin(_, client, message: Message):
    """Check if the user is an admin in the chat."""
    admins = await mp.get_admins(CHAT_ID)
    if message.from_user is None and message.sender_chat:
        return True
    return message.from_user.id in admins

# Create a custom filter for admin commands
ADMINS_FILTER = filters.create(is_admin)

@Client.on_message(filters.command(["radio", f"radio@{USERNAME}"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def radio(_, message: Message):
    """Start the radio stream if not already running."""
    if 1 in RADIO:
        response_msg = await message.reply_text(f"{emoji.ROBOT} **Please Stop Existing Radio Stream!**")
        await mp.delete(response_msg)
        await message.delete()
        return

    await mp.start_radio()
    response_msg = await message.reply_text(f"{emoji.CHECK_MARK_BUTTON} **Radio Stream Started :** \n<code>{STREAM}</code>")
    await mp.delete(response_msg)
    await mp.delete(message)

@Client.on_message(filters.command(["stopradio", f"stopradio@{USERNAME}"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def stop(_, message: Message):
    """Stop the radio stream if it is currently running."""
    if 0 in RADIO:
        response_msg = await message.reply_text(f"{emoji.ROBOT} **Please Start A Radio Stream First!**")
        await mp.delete(response_msg)
        await mp.delete(message)
        return

    await mp.stop_radio()
    response_msg = await message.reply_text(f"{emoji.CROSS_MARK_BUTTON} **Radio Stream Ended Successfully!**")
    await mp.delete(response_msg)
    await mp.delete(message)

