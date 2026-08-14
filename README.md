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
     - `DISCORD_WEBHOOK_URL`
3. The workflow runs automatically every 6 hours (you can also trigger it manually from the Actions tab)

### Discord webhook setup

1. In Discord: **Server Settings → Integrations → Webhooks → New Webhook**
2. Pick a name (e.g. "Epic Free Games"), select the target channel, and **Copy Webhook URL**
3. Add that URL as the `DISCORD_WEBHOOK_URL` secret

That's it — no bot account or permissions needed. A webhook is also more reliable here, since the bot API is often blocked by Cloudflare when called from GitHub Actions' datacenter IPs.

Built with Python, GitHub Actions, the Telegram Bot API, and the Discord API.
