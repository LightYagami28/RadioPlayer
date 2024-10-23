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

import os
import time
import requests
import yt_dlp
from config import Config
from utils import USERNAME, mp
from pyrogram.types import Message
from pyrogram import Client, filters
from youtube_search import YoutubeSearch

# Configuration variables
CHAT_ID = Config.CHAT_ID
LOG_GROUP = Config.LOG_GROUP

## Extra Functions -------------------------------

def time_to_seconds(time_str):
    """Convert hh:mm:ss to seconds."""
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time_str).split(':'))))

## Commands --------------------------------

@Client.on_message(filters.command(["song", f"song@{USERNAME}"]) & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def song(_, message: Message):
    """Search and download a song from YouTube."""
    query = ' '.join(message.command[1:])
    print(query)

    # Notify user about the search
    k = await message.reply_text("🔍 **Searching Song...**")
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "geo-bypass": True,
        "nocheckcertificate": True,
        "outtmpl": "downloads/%(id)s.%(ext)s",
    }

    try:
        results = []
        count = 0

        # Search for the song
        while len(results) == 0 and count < 6:
            if count > 0:
                await asyncio.sleep(1)  # Wait a second before retrying
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1

        if not results:
            await k.edit('❌ **Found Literally Nothing! \nPlease Try Another Song or Use Correct Spelling.**')
            return

        # Extract video information
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        views = results[0]["views"]

        # Download thumbnail
        thumb_name = f'thumb{message.message_id}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        with open(thumb_name, 'wb') as thumb_file:
            thumb_file.write(thumb.content)

    except Exception as e:
        await k.edit("❗ **Enter A Song Name!** \nFor Example: `/song Alone Marshmellow`")
        print(str(e))
        return

    await k.edit("📥 **Downloading Song...**")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        # Prepare the caption for the audio message
        cap = (f'🏷 <b>Title:</b> <a href="{link}">{title}</a>\n'
               f'⏳ <b>Duration:</b> <code>{duration}</code>\n'
               f'👀 <b>Views:</b> <code>{views}</code>\n'
               f'🎧 <b>Requested By:</b> {message.from_user.mention()} \n'
               f'📤 <b>Uploaded By: <a href="https://t.me/AsmSafone">🇧🇩 Ｓ１ ＢＯＴＳ</a></b>')

        # Convert duration to seconds
        dur = time_to_seconds(duration)

        await k.edit("📤 **Uploading Song...**")
        await message.reply_audio(audio_file, caption=cap, parse_mode='HTML', title=title, duration=dur, performer="[ꜱᴀꜰᴏɴᴇ ᴍᴜꜱɪᴄ]", thumb=thumb_name)
        await k.delete()
        await mp.delete(message)

    except Exception as e:
        await k.edit(f'❌ **An Error Occurred!** \n\nError: {e}')
        print(e)

    # Clean up downloaded files
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
