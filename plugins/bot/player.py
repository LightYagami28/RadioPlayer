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
import re
import ffmpeg
import asyncio
import subprocess
from config import Config
from signal import SIGINT
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from pyrogram import Client, filters, emoji
from utils import mp, RADIO, USERNAME, FFMPEG_PROCESSES
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Configuration variables
msg = Config.msg
playlist = Config.playlist
ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
LOG_GROUP = Config.LOG_GROUP
RADIO_TITLE = Config.RADIO_TITLE
EDIT_TITLE = Config.EDIT_TITLE
ADMIN_ONLY = Config.ADMIN_ONLY
DURATION_LIMIT = Config.DURATION_LIMIT

# Check if the user is an admin
async def is_admin(_, client, message: Message):
    admins = await mp.get_admins(CHAT_ID)
    if message.from_user is None and message.sender_chat:
        return True
    return message.from_user.id in admins

ADMINS_FILTER = filters.create(is_admin)

# Command to play audio or video
@Client.on_message(filters.command(["play", f"play@{USERNAME}"]) & 
                    (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)) | 
                    filters.audio & filters.private)
async def yplay(_, message: Message):
    if ADMIN_ONLY == "True":
        admins = await mp.get_admins(CHAT_ID)
        if message.from_user.id not in admins:
            m = await message.reply_sticker("CAACAgUAAxkBAAEBpyZhF4R-ZbS5HUrOxI_MSQ10hQt65QACcAMAApOsoVSPUT5eqj5H0h4E")
            await mp.delete(m)
            await mp.delete(message)
            return
            
    type = ""
    yturl = ""
    ysearch = ""
    if message.audio:
        type = "audio"
        m_audio = message
    elif message.reply_to_message and message.reply_to_message.audio:
        type = "audio"
        m_audio = message.reply_to_message
    else:
        if message.reply_to_message:
            link = message.reply_to_message.text
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex, link)
            if match:
                type = "youtube"
                yturl = link
        elif " " in message.text:
            text = message.text.split(" ", 1)
            query = text[1]
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex, query)
            if match:
                type = "youtube"
                yturl = query
            else:
                type = "query"
                ysearch = query
        else:
            d = await message.reply_text("❗️ __You Didn't Give Me Anything To Play, Send Me An Audio File or Reply /play To An Audio File!__")
            await mp.delete(d)
            await mp.delete(message)
            return
            
    user = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    group_call = mp.group_call

    # Handling audio files
    if type == "audio":
        if round(m_audio.audio.duration / 60) > DURATION_LIMIT:
            d = await message.reply_text(f"❌ __Audios Longer Than {DURATION_LIMIT} Minute(s) Aren't Allowed, The Provided Audio Is {round(m_audio.audio.duration/60)} Minute(s)!__")
            await mp.delete(d)
            await mp.delete(message)
            return
        if playlist and playlist[-1][2] == m_audio.audio.file_id:
            d = await message.reply_text(f"➕ **Already Added To Playlist!**")
            await mp.delete(d)
            await mp.delete(message)
            return

        data = {1: m_audio.audio.title, 2: m_audio.audio.file_id, 3: "telegram", 4: user}
        playlist.append(data)
        
        # Start playing the first track
        if len(playlist) == 1:
            m_status = await message.reply_text("⚡️")
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT_ID)
                if process:
                    try:
                        process.send_signal(SIGINT)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    except Exception as e:
                        print(e)
                        pass
                    FFMPEG_PROCESSES[CHAT_ID] = ""
                    
            if not group_call.is_connected:
                await mp.start_call()
                
            file = playlist[0][1]
            group_call.input_filename = os.path.join(
                _.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )
            await m_status.delete()
            print(f"- START PLAYING: {playlist[0][1]}")
            
        # Displaying the playlist
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:   
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
            ])
            
        if EDIT_TITLE:
            await mp.edit_title()
        
        if message.chat.type == "private":
            await message.reply_text(pl)        
        elif LOG_GROUP:
            await mp.send_playlist()
        elif not LOG_GROUP and message.chat.type == "supergroup":
            k = await message.reply_text(pl)
            await mp.delete(k)
            
        for track in playlist[:2]:
            await mp.download_audio(track)

    # Handling YouTube URLs and queries
    if type == "youtube" or type == "query":
        if type == "youtube":
            msg = await message.reply_text("🔍")
            url = yturl
        elif type == "query":
            try:
                msg = await message.reply_text("🔍")
                ytquery = ysearch
                results = YoutubeSearch(ytquery, max_results=1).to_dict()
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
            except Exception as e:
                await msg.edit("**Literally Found Nothing!\nTry Searching On Inline 😉!**")
                print(str(e))
                return
            await mp.delete(message)
        else:
            return
        
        ydl_opts = {
            "geo-bypass": True,
            "nocheckcertificate": True
        }
        ydl = YoutubeDL(ydl_opts)
        
        try:
            info = ydl.extract_info(url, False)
        except Exception as e:
            print(e)
            k = await msg.edit(f"❌ **YouTube Download Error !** \n\n{e}")
            print(str(e))
            await mp.delete(message)
            await mp.delete(k)
            return
            
        duration = round(info["duration"] / 60)
        title = info["title"]
        if int(duration) > DURATION_LIMIT:
            k = await message.reply_text(f"❌ __Videos Longer Than {DURATION_LIMIT} Minute(s) Aren't Allowed, The Provided Video Is {duration} Minute(s)!__")
            await mp.delete(k)
            await mp.delete(message)
            return
            
        data = {1: title, 2: url, 3: "youtube", 4: user}
        playlist.append(data)
        group_call = mp.group_call
        client = group_call.client
        
        # Start playing the first track
        if len(playlist) == 1:
            m_status = await msg.edit("⚡️")
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT_ID)
                if process:
                    try:
                        process.send_signal(SIGINT)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    except Exception as e:
                        print(e)
                        pass
                    FFMPEG_PROCESSES[CHAT_ID] = ""
                    
            if not group_call.is_connected:
                await mp.start_call()
                
            file = playlist[0][1]
            group_call.input_filename = os.path.join(
                _.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )
            await m_status.delete()
            print(f"- START PLAYING: {playlist[0][1]}")

        # Displaying the playlist
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
            ])

        if EDIT_TITLE:
            await mp.edit_title()
        
        if message.chat.type == "private":
            await message.reply_text(pl)        
        elif LOG_GROUP:
            await mp.send_playlist()
        elif not LOG_GROUP and message.chat.type == "supergroup":
            k = await message.reply_text(pl)
            await mp.delete(k)

        for track in playlist[:2]:
            await mp.download_audio(track)
