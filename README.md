# Telegram Radio Player V3 [![Mentioned in Awesome Telegram Calls](https://awesome.re/mentioned-badge-flat.svg)](https://github.com/tgcalls/awesome-tgcalls)
![GitHub Repo stars](https://img.shields.io/github/stars/LightYagami28/RadioPlayer?color=blue&style=flat)
![GitHub forks](https://img.shields.io/github/forks/LightYagami28/RadioPlayer?color=green&style=flat)
![GitHub issues](https://img.shields.io/github/issues/LightYagami28/RadioPlayer)
![GitHub closed issues](https://img.shields.io/github/issues-closed/LightYagami28/RadioPlayer)
![GitHub pull requests](https://img.shields.io/github/issues-pr/LightYagami28/RadioPlayer)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/LightYagami28/RadioPlayer)
![GitHub contributors](https://img.shields.io/github/contributors/LightYagami28/RadioPlayer?style=flat)
![GitHub repo size](https://img.shields.io/github/repo-size/LightYagami28/RadioPlayer?color=red)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/LightYagami28/RadioPlayer)

An advanced Telegram bot to play nonstop radio, music, or YouTube Live in channel or group voice chats.

## Special Features

- Playlist, queue, and 24/7 radio stream
- Supports live streaming from YouTube
- Automatically starts radio if no songs are in the playlist
- Automatic playback even if Heroku restarts
- Displays the current playing position of the audio
- Controls with buttons and commands
- Downloads songs from YouTube as audio
- Changes the voice chat title to the currently playing song name
- Automatically downloads audio for the first two tracks in the playlist to ensure smooth playback

## Deploy to Heroku

<p><a href="https://deploy.safone.tech/"><img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200"/></a></p>

**NOTE:** Change the app region to Europe to improve bot stability.

## Deploy to Railway

<p><a href="https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2FAsmSafone%2FRadioPlayerV3&envs=API_ID%2CAPI_HASH%2CBOT_TOKEN%2CSESSION_STRING%2CCHAT_ID%2CLOG_GROUP%2CADMINS%2CADMIN_ONLY%2CMAXIMUM_DURATION%2CSTREAM_URL%2CREPLY_MESSAGE&optionalEnvs=LOG_GROUP%2CADMIN_ONLY%2CMAXIMUM_DURATION%2CSTREAM_URL%2CREPLY_MESSAGE&API_IDDesc=Your+Telegram+API_ID+get+it+from+my.telegram.org%2Fapps&API_HASHDesc=Your+Telegram+API_HASH+get+it+from+my.telegram.org%2Fapps&BOT_TOKENDesc=Bot+token+of+your+bot%2C+get+from+%40Botfather&SESSION_STRINGDesc=Session+string%2C+use+%40genStr_robot+to+generate+pyrogram+session+string&CHAT_IDDesc=ID+of+Channel+or+Group+where+the+Bot+plays+Radio%2FMusic%2FYouTube+Lives&LOG_GROUPDesc=ID+of+the+group+to+send+playlist+if+CHAT+is+a+Group%2C+if+channel+then+leave+blank&ADMINSDesc=ID+of+Users+who+can+use+Admin+commands+%28for+multiple+users+seperated+by+space%29&ADMIN_ONLYDesc=Change+it+to+%27True%27+If+you+want+to+make+%2Fplay+commands+only+for+admins+of+CHAT.+By+default+%2Fplay+is+available+for+all.&MAXIMUM_DURATIONDesc=Maximum+duration+of+song+to+be+played+using+%2Fplay+command&STREAM_URLDesc=URL+of+Radio+station+or+Youtube+Live+video+url+to+stream+with+%2Fradio+command&REPLY_MESSAGEDesc=A+reply+message+to+those+who+message+the+USER+account+in+PM.+Make+it+blank+if+you+do+not+need+this+feature.&MAXIMUM_DURATIONDefault=15&ADMIN_ONLYDefault=False&STREAM_URLDefault=https://youtu.be/5qap5aO4i9A&REPLY_MESSAGEDefault=Hello Sir, I'm a bot to play radio/music/youtube live on telegram voice chat, not having time to chat with you 😂!"> <img src="https://img.shields.io/badge/Deploy%20To%20Railway-blueviolet?style=for-the-badge&logo=railway" width="200"/></a></p>

**NOTE:** Make sure you have started a voice chat in your channel/group before deploying!

## Config Vars:

1. `API_ID`: Get it from [my.telegram.org/apps](https://my.telegram.org/apps)
2. `API_HASH`: Get it from [my.telegram.org/apps](https://my.telegram.org/apps)
3. `BOT_TOKEN`: Get it from [@Botfather](https://t.me/botfather)
4. `SESSION_STRING`: Generate from [@genStr robot](http://t.me/genStr_robot) or [![genStr](https://img.shields.io/badge/repl.it-genStr-yellowgreen)](https://repl.it/@AsmSafone/genStr)
5. `CHAT_ID`: ID of the channel/group where the bot plays music/radio.
6. `LOG_GROUP`: ID of the group to send the playlist if `CHAT_ID` is a group.
7. `AUTH_USERS`: ID of authorized users who can use admin commands (for multiple users, separate with space).
8. `STREAM_URL`: Stream URL of the radio station or a YouTube live video to stream when the bot starts or with the `/radio` command. Here are [Some Live Streaming Links](https://telegra.ph/Live-Radio-Stream-Links-05-17).
9. `MAXIMUM_DURATION`: Maximum duration of the song to play (optional).
10. `REPLY_MESSAGE`: A reply to those who message the USER account in PM. Leave it blank if you do not need this feature.
11. `ADMIN_ONLY`: Set to `'True'` if you want to restrict `/play` commands to admins of the chat. By default, `/play` is available for all.
12. `HEROKU_API_KEY`: Your Heroku API key. Get it from [here](https://dashboard.heroku.com/account).
13. `HEROKU_APP_NAME`: Name of your Heroku app if deploying to Heroku.

- Enable the worker after deploying the project to Heroku.
- The bot will automatically start the radio in the given `CHAT_ID` with the specified `STREAM_URL` after deployment. 
- It will provide 24/7 music even if Heroku restarts, as the radio stream restarts automatically.
- To play a song, use `/play` as a reply to an audio file or a YouTube link, or use `/play [song name]`.
- Use `/help` to know about other commands and their usage.

## Requirements

- Python 3.6 or higher
- [Telegram API Key](https://docs.pyrogram.org/intro/quickstart#enjoy-the-api)
- [FFmpeg](https://www.ffmpeg.org/)
- Telegram [String Session](http://t.me/genStr_robot) of the account
- User accounts must be admins in the channel or group
- Must start a voice chat in the channel/group before running the bot

## Run On VPS

```sh
$ git clone https://github.com/LightYagami28/RadioPlayer
$ cd RadioPlayerV3
$ sudo apt install git curl python3-pip ffmpeg -y
$ pip3 install --upgrade pip
$ pip3 install -r requirements.txt
# <create .env variables appropriately>
$ python3 main.py
```

## License

```sh
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021 Asm Safone <https://github.com/AsmSafone>
RadioPlayer, Telegram Voice Chat Bot
Copyright (c) 2024 Light Yagami <https://github.com/LightYagami28>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>
```

## Credits

- [Asm Safone](https://github.com/Asm

Safone) for [Noting](https://github.com/AsmSafone/RadioPlayerV3) 😬
- [Dan](https://github.com/delivrance) for [Pyrogram](https://github.com/pyrogram/pyrogram) ❤️
- [MarshalX](https://github.com/MarshalX) for [pytgcalls](https://github.com/MarshalX/tgcalls) ❤️
- And thanks to all [contributors](https://github.com/AsmSafone/RadioPlayerV3/graphs/contributors)! ❤️
