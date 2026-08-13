# Epic Free Games Watcher

A bot that notifies you when Epic Games Store releases new free games — on Telegram and/or Discord.

## How it works

- Checks the Epic Games Store API every 6 hours
- Notifies you of new **currently free** games and **upcoming free** games
- Runs on GitHub Actions (free, cloud-based, no PC needed)
- Sends notifications via Telegram and/or Discord

## Notifications

- 🎮 Free NOW games — available right now
- 🔮 Upcoming free games — coming next week

## Setup

1. Create a GitHub repo and upload these files
2. Add secrets in Settings → Secrets and variables → Actions:
   - Telegram (optional — only if you want Telegram notifications):
     - `TELEGRAM_BOT_TOKEN`
     - `TELEGRAM_CHAT_ID`
   - Discord (optional — only if you want Discord notifications):
     - `DISCORD_BOT_TOKEN`
     - `DISCORD_CHANNEL_ID`
3. The workflow runs automatically every 6 hours (you can also trigger it manually from the Actions tab)

### Discord bot setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**, give it a name, and open it
2. Go to the **Bot** tab → **Reset Token** and copy the token (this is your `DISCORD_BOT_TOKEN`)
3. Go to **OAuth2 → URL Generator**:
   - Under **Scopes**, tick **bot**
   - Under **Bot Permissions**, tick **Send Messages**
   - Copy the generated URL, open it, and invite the bot to your server
4. Enable **Developer Mode** (Discord User Settings → Advanced), right-click the target channel → **Copy Channel ID** (this is your `DISCORD_CHANNEL_ID`)

> No privileged intents are required — the bot only uses the REST API to post messages.

Set `DISCORD_BOT_TOKEN` and `DISCORD_CHANNEL_ID` as secrets, and you're done.

Built with Python, GitHub Actions, the Telegram Bot API, and the Discord API.
