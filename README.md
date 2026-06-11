# Epic Free Games Watcher

A Telegram bot that notifies you when Epic Games Store releases new free games.

## How it works

- Checks the Epic Games Store API every 6 hours
- Notifies you of new **currently free** games and **upcoming free** games
- Runs on GitHub Actions (free, cloud-based, no PC needed)
- Sends notifications via Telegram

## Notifications

- 🎮 Free NOW games — available right now
- 🔮 Upcoming free games — coming next week

## Setup

1. Create a GitHub repo and upload these files
2. Add secrets in Settings → Secrets → Actions:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. The workflow runs automatically every 6 hours

Built with Python, GitHub Actions, and Telegram Bot API.
