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
from config import Config
from utils import USERNAME, mp
from pyrogram import Client, filters, emoji
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Configuration variables
msg = Config.msg
ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
playlist = Config.playlist
LOG_GROUP = Config.LOG_GROUP

# Text messages for bot interactions
HOME_TEXT = (
    "👋🏻 **Hi [{}](tg://user?id={})**, \n\n"
    "I'm **Radio Player V3.0** \nI Can Play Radio / Music / YouTube Live In Channel & Group 24x7 Nonstop. Made with ❤️ By @AsmSafone 😉!"
)
HELP_TEXT = """
💡 --**Setting Up**--:
• Add the bot and user account in your group with admin rights.
• Start a voice chat in your group & restart the bot if not joined to vc.
• Use /play [song name] or use /play as a reply to an audio file or YouTube link.

💡 --**Common Commands**--:
• `/help` - shows help for all commands
• `/song` [song name] - download the song as audio
• `/current` - shows current track with controls
• `/playlist` - shows the current & queued playlist

💡 --**Admins Commands**--:
• `/radio` - start radio stream
• `/stopradio` - stop radio stream
• `/skip` - skip current music
• `/join` - join the voice chat
• `/leave` - leave the voice chat
• `/stop` - stop playing music
• `/volume` - change volume (0-200)
• `/replay` - play from the beginning
• `/clean` - remove unused raw files
• `/pause` - pause playing music
• `/resume` - resume playing music
• `/mute` - mute the vc userbot
• `/unmute` - unmute the vc userbot
• `/restart` - update & restart the bot
• `/setvar` - set/change Heroku configs

© **Powered By** : 
**@AsmSafone | @AsmSupport** 👑
"""

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    """Handles callback queries from inline buttons."""
    
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer("You're Not Allowed! 🤣", show_alert=True)
        return

    # Command handling based on the user's query
    if query.data.lower() == "replay":
        await handle_replay(query)
    elif query.data.lower() == "pause":
        await handle_pause(query)
    elif query.data.lower() == "resume":
        await handle_resume(query)
    elif query.data.lower() == "skip":
        await handle_skip(query)
    elif query.data.lower() == "help":
        await show_help(query)
    elif query.data.lower() == "home":
        await show_home(query)
    elif query.data.lower() == "close":
        await close_menu(query)

    await query.answer()

async def handle_replay(query):
    """Handles replaying the current track."""
    group_call = mp.group_call
    if not playlist:
        await query.answer("⛔️ Empty Playlist !", show_alert=True)
        return

    group_call.restart_playout()
    await update_playlist_message(query, "🔂 Replaying !")

async def handle_pause(query):
    """Handles pausing the current track."""
    if not playlist:
        await query.answer("⛔️ Empty Playlist !", show_alert=True)
        return

    mp.group_call.pause_playout()
    await update_playlist_message(query, "⏸ Paused !")

async def handle_resume(query):
    """Handles resuming the current track."""
    if not playlist:
        await query.answer("⛔️ Empty Playlist !", show_alert=True)
        return

    mp.group_call.resume_playout()
    await update_playlist_message(query, "▶️ Resumed !")

async def handle_skip(query):
    """Handles skipping the current track."""
    if not playlist:
        await query.answer("⛔️ Empty Playlist !", show_alert=True)
        return

    await mp.skip_current_playing()
    await update_playlist_message(query, "⏩ Skipped !")

async def update_playlist_message(query, action_message):
    """Updates the playlist message after a user action."""
    pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
        f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
        for i, x in enumerate(playlist)
    ])

    try:
        await query.answer(action_message, show_alert=True)
        await query.edit_message_text(
            pl,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏸", callback_data="pause"),
                        InlineKeyboardButton("⏩", callback_data="skip")
                    ],
                ]
            )
        )
    except MessageNotModified:
        pass

async def show_help(query):
    """Displays help information to the user."""
    buttons = [
        [InlineKeyboardButton("SEARCH SONGS INLINE", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
         InlineKeyboardButton("SUPPORT", url="https://t.me/AsmSupport")],
        [InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
         InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3")],
        [InlineKeyboardButton("BACK HOME", callback_data="home"),
         InlineKeyboardButton("CLOSE MENU", callback_data="close")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    try:
        await query.edit_message_text(HELP_TEXT, reply_markup=reply_markup)
    except MessageNotModified:
        pass

async def show_home(query):
    """Displays the home message to the user."""
    buttons = [
        [InlineKeyboardButton("SEARCH SONGS INLINE", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
         InlineKeyboardButton("SUPPORT", url="https://t.me/AsmSupport")],
        [InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
         InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3")],
        [InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    try:
        await query.edit_message_text(
            HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
            reply_markup=reply_markup
        )
    except MessageNotModified:
        pass

async def close_menu(query):
    """Closes the menu by deleting the current message."""
    try:
        await query.message.delete()
        await query.message.reply_to_message.delete()
    except Exception as e:
        print(f"Error closing menu: {e}")

@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
    """Handles the start command."""
    buttons = [
        [InlineKeyboardButton("SEARCH SONGS INLINE", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
         InlineKeyboardButton("SUPPORT", url="https://t.me/AsmSupport")],
        [InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
         InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3")],
        [InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m = await message.reply_photo(
        photo="https://telegra.ph/file/4e839766d45935998e9c6.jpg",
        caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id),
        reply_markup=reply_markup
    )
    await mp.delete(m)
    await mp.delete(message)

@Client.on_message(filters.command(["help", f"help@{USERNAME}"]))
async def help(client, message):
    """Handles the help command."""
    buttons = [
        [InlineKeyboardButton("SEARCH SONGS INLINE", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
         InlineKeyboardButton("SUPPORT", url="https://t.me/AsmSupport")],
        [InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
         InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3")],
        [InlineKeyboardButton("BACK HOME", callback_data="home"),
         InlineKeyboardButton("CLOSE MENU", callback_data="close")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(HELP_TEXT, reply_markup=reply_markup)

async def handle_message(client, message):
    """Processes incoming messages."""
    if message.text:
        # Custom logic can be added here for processing text messages.
        pass

@Client.on_message(filters.all)
async def message_handler(client, message):
    """Handler for all messages, delegating processing."""
    await handle_message(client, message)

if __name__ == "__main__":
    asyncio.run(Client.run())
