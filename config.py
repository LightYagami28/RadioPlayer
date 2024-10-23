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
import sys
import heroku3
import subprocess
from dotenv import load_dotenv
from yt_dlp import YoutubeDL  # Assuming yt-dlp is correctly installed

# Load environment variables from .env file
load_dotenv()

# YouTube downloader options
ydl_opts = {
    "geo-bypass": True,
    "nocheckcertificate": True
}
ydl = YoutubeDL(ydl_opts)

# Initialize variables
links = []
finalurl = ""
STREAM = os.environ.get("STREAM_URL", "http://peridot.streamguys.com:7150/Mirchi")
regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"

# Check if the STREAM URL is a YouTube link
if re.match(regex, STREAM):
    meta = ydl.extract_info(STREAM, download=False)
    formats = meta.get('formats', [meta])
    links = [f['url'] for f in formats]  # Extract all formats URLs
    finalurl = links[0] if links else STREAM
else:
    finalurl = STREAM

class Config:
    # Mandatory Variables
    ADMIN = os.environ.get("AUTH_USERS", "")
    ADMINS = [int(admin) if re.search('^\d+$', admin) else admin for admin in ADMIN.split()]
    ADMINS.append(1316963576)  # Add your admin ID here
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    CHAT_ID = int(os.environ.get("CHAT_ID", ""))
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    SESSION = os.environ.get("SESSION_STRING", "")

    # Optional Variables
    STREAM_URL = finalurl
    LOG_GROUP = int(os.environ.get("LOG_GROUP", "")) if os.environ.get("LOG_GROUP") else None
    ADMIN_ONLY = os.environ.get("ADMIN_ONLY", "False") == "True"
    REPLY_MESSAGE = os.environ.get("REPLY_MESSAGE", None)
    DELAY = int(os.environ.get("DELAY", 10))
    EDIT_TITLE = os.environ.get("EDIT_TITLE", "True") == "True"
    RADIO_TITLE = os.environ.get("RADIO_TITLE", "RADIO 24/7 | LIVE") or None
    DURATION_LIMIT = int(os.environ.get("MAXIMUM_DURATION", 15))

    # Extra Variables (For Heroku)
    API_KEY = os.environ.get("HEROKU_API_KEY", None)
    APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    HEROKU_APP = heroku3.from_key(API_KEY).apps()[APP_NAME] if API_KEY and APP_NAME else None

    # Temp DB Variables (Don't Touch)
    msg = {}
    playlist = []
