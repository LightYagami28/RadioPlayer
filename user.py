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

from config import Config
from pyrogram import Client

# Determine if the user client should have reply message capabilities
user_client_options = {
    "session_name": Config.SESSION,
    "api_id": Config.API_ID,
    "api_hash": Config.API_HASH,
    "plugins": {"root": "plugins.userbot"} if Config.REPLY_MESSAGE is not None else None
}

# Create and start the user client
USER = Client(**{k: v for k, v in user_client_options.items() if v is not None})
USER.start()
