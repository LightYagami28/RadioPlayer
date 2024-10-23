"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>
"""

import os
import sys
import wget
import ffmpeg
import asyncio
import subprocess
from os import path
from signal import SIGINT
from random import randint
from pyrogram import Client, emoji
from pyrogram.errors import FloodWait
from pytgcalls import GroupCallFactory
from pytgcalls.exceptions import GroupCallNotFoundError
from yt_dlp import YoutubeDL
from pyrogram.raw.types import InputGroupCall
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR

# Check for required modules and install if missing
try:
    from config import Config
except ModuleNotFoundError:
    file = os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)

# Initialize bot and configuration
bot = Client("RadioPlayerVC", Config.API_ID, Config.API_HASH, bot_token=Config.BOT_TOKEN)
bot.start()

e = bot.get_me()
USERNAME = e.username

# Constants and global variables
ADMINS = Config.ADMINS
STREAM_URL = Config.STREAM_URL
CHAT_ID = Config.CHAT_ID
ADMIN_LIST = {}
CALL_STATUS = {}
FFMPEG_PROCESSES = {}
RADIO = {6}
LOG_GROUP = Config.LOG_GROUP
DURATION_LIMIT = Config.DURATION_LIMIT
DELAY = Config.DELAY
playlist = Config.playlist
msg = Config.msg
EDIT_TITLE = Config.EDIT_TITLE
RADIO_TITLE = Config.RADIO_TITLE

# YouTube DL options
ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)

class MusicPlayer:
    def __init__(self):
        self.group_call = GroupCallFactory(USER, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_file_group_call()

    async def send_playlist(self):
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join(
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}\n" for i, x in enumerate(playlist)
            )
        if msg.get('playlist') is not None:
            await msg['playlist'].delete()
        msg['playlist'] = await self.send_text(pl)

    async def skip_current_playing(self):
        if not playlist:
            return
        if len(playlist) == 1:
            await self.start_radio()
            return

        old_track = playlist.pop(0)
        print(f"- START PLAYING: {playlist[0][1]}")

        if EDIT_TITLE:
            await self.edit_title()
        if LOG_GROUP:
            await self.send_playlist()

        # Remove the old track file
        download_dir = os.path.join(self.group_call.client.workdir, DEFAULT_DOWNLOAD_DIR)
        os.remove(os.path.join(download_dir, f"{old_track[1]}.raw"))

        await self.download_audio(playlist[1])

    async def send_text(self, text):
        chat_id = LOG_GROUP
        message = await bot.send_message(
            chat_id,
            text,
            disable_web_page_preview=True,
            disable_notification=True
        )
        return message

    async def download_audio(self, song):
        raw_file = os.path.join(self.group_call.client.workdir, DEFAULT_DOWNLOAD_DIR, f"{song[1]}.raw")
        
        if not os.path.isfile(raw_file):
            original_file = await self.get_original_file(song)
            if original_file:
                self.convert_to_raw(original_file, raw_file)
                os.remove(original_file)

    async def get_original_file(self, song):
        if song[3] == "telegram":
            return await bot.download_media(f"{song[2]}")
        elif song[3] == "youtube":
            url = song[2]
            try:
                info = ydl.extract_info(url, False)
                ydl.download([url])
                return path.join("downloads", f"{info['id']}.{info['ext']}")
            except Exception as e:
                playlist.pop(1)
                print(f"Unable to download due to {e} & skipped!")
                if len(playlist) == 1:
                    return None
                await self.download_audio(playlist[1])
                return None
        else:
            return wget.download(song[2])

    def convert_to_raw(self, original_file, raw_file):
        ffmpeg.input(original_file).output(
            raw_file,
            format='s16le',
            acodec='pcm_s16le',
            ac=2,
            ar='48k',
            loglevel='error'
        ).overwrite_output().run()

    async def start_radio(self):
        if self.group_call.is_connected:
            playlist.clear()

        process = FFMPEG_PROCESSES.get(CHAT_ID)
        if process:
            self.stop_process(process)

        self.setup_radio_stream()
        await self.connect_to_call()

    def stop_process(self, process):
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(e)

    def setup_radio_stream(self):
        station_stream_url = STREAM_URL
        if os.path.exists(f'radio-{CHAT_ID}.raw'):
            os.remove(f'radio-{CHAT_ID}.raw')
        os.mkfifo(f'radio-{CHAT_ID}.raw')
        self.group_call.input_filename = f'radio-{CHAT_ID}.raw'

    async def connect_to_call(self):
        ffmpeg_log = open("ffmpeg.log", "w+")
        command = [
            "ffmpeg", "-y", "-i", STREAM_URL,
            "-f", "s16le", "-ac", "2", "-ar", "48000",
            "-acodec", "pcm_s16le", self.group_call.input_filename
        ]

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=ffmpeg_log,
            stderr=asyncio.subprocess.STDOUT,
        )

        FFMPEG_PROCESSES[CHAT_ID] = process
        if RADIO_TITLE:
            await self.edit_title()

        await asyncio.sleep(2)
        await self.wait_for_connection()

    async def wait_for_connection(self):
        while True:
            if self.group_call.is_connected:
                print("Successfully joined VC!")
                break
            else:
                print("Connecting, please wait...")
                await self.start_call()
                await asyncio.sleep(10)

    async def stop_radio(self):
        if self.group_call:
            playlist.clear()
            self.group_call.input_filename = ''
            process = FFMPEG_PROCESSES.get(CHAT_ID)
            if process:
                self.stop_process(process)
            try:
                RADIO.remove(1)
            except KeyError:
                pass

    async def start_call(self):
        try:
            await self.group_call.start(CHAT_ID)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            if not self.group_call.is_connected:
                await self.group_call.start(CHAT_ID)
        except GroupCallNotFoundError:
            await self.create_group_call()
        except Exception as e:
            print(e)

    async def create_group_call(self):
        try:
            await USER.send(CreateGroupCall(
                peer=(await USER.resolve_peer(CHAT_ID)),
                random_id=randint(10000, 999999999)
            ))
            await self.group_call.start(CHAT_ID)
        except Exception as e:
            print(e)

    async def edit_title(self):
        title = RADIO_TITLE if not playlist else playlist[0][1]
        call = InputGroupCall(id=self.group_call.group_call.id, access_hash=self.group_call.group_call.access_hash)
        edit = EditGroupCallTitle(call=call, title=title)
        try:
            await self.group_call.client.send(edit)
        except Exception as e:
            print("Error occurred while changing VC title:", e)

    async def delete(self, message):
        if message.chat.type == "supergroup":
            await asyncio.sleep(DELAY)
            try:
                await message.delete()
            except Exception:
                pass

    async def get_admins(self, chat):
        admins = ADMIN_LIST.get(chat)
        if not admins:
            admins = Config.ADMINS + [1316963576]
            try:
                grpadmins = await bot.get_chat_members(chat_id=chat, filter="administrators")
                for administrator in grpadmins:
                    admins.append(administrator.user.id)
            except Exception as e:
                print(e)
            ADMIN_LIST[chat] = admins

mp = MusicPlayer()

# Pytgcalls handlers
@mp.group_call.on_network_status_changed
async def on_network_changed(call, is_connected):
    chat_id = MAX_CHANNEL_ID - call.full_chat.id
    CALL_STATUS[chat_id] = is_connected

@mp.group_call.on_playout_ended
async def playout_ended_handler(_, __):
    if not playlist:
        await mp.start_radio()
    else:
        await mp.skip_current_playing()
