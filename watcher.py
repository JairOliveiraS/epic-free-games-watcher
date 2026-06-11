import os
import json
import time
import urllib.request
import urllib.error

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SEEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seen_games.json")
EPIC_API = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=pt-BR&country=BR&allowCountries=BR"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    return {"seen_current": [], "seen_upcoming": []}


def save_seen(data):
    with open(SEEN_FILE, "w") as f:
        json.dump(data, f, indent=2)


def fetch_free_games():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(EPIC_API, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("[ERROR] Failed to fetch Epic API: " + str(e))
        return [], []

    current_free = []
    upcoming_free = []

    for game in data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", []):
        title = game.get("title", "Unknown")
        slug = game.get("productSlug", "") or game.get("urlSlug", "")
        if not slug:
            continue

        promos = game.get("promotions", {})
        if not promos:
            continue

        # Check current free games
        for offer in promos.get("promotionalOffers", []):
            for promo in offer.get("promotionalOffers", []):
                if promo.get("discountPercentage") in (0, None):
                    start = promo.get("startDate", "")[:10]
                    end = promo.get("endDate", "")[:10]
                    current_free.append({"title": title, "slug": slug, "start": start, "end": end, "id": slug})

        # Check upcoming free games
        for offer in promos.get("upcomingPromotionalOffers", []):
            for promo in offer.get("promotionalOffers", []):
                if promo.get("discountPercentage") in (0, None):
                    start = promo.get("startDate", "")[:10]
                    end = promo.get("endDate", "")[:10]
                    upcoming_free.append({"title": title, "slug": slug, "start": start, "end": end, "id": slug})

    return current_free, upcoming_free


def send_telegram(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[ERROR] TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set.")
        return False
    url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("ok"):
                print("[OK] Telegram message sent.")
                return True
            else:
                print("[ERROR] Telegram API returned: " + str(result))
                return False
    except Exception as e:
        print("[ERROR] Failed to send Telegram message: " + str(e))
        return False


def main():
    seen = load_seen()
    seen_current = set(seen.get("seen_current", []))
    seen_upcoming = set(seen.get("seen_upcoming", []))

    print("[INFO] Checking Epic Games Store for free games...")
    current_free, upcoming_free = fetch_free_games()

    # Check for new CURRENTLY free games
    new_current = [g for g in current_free if g["id"] not in seen_current]
    if new_current:
        print("[INFO] Found " + str(len(new_current)) + " new FREE game(s)!")
        for game in new_current:
            url = "https://store.epicgames.com/p/" + game["slug"]
            msg = (
                "\U0001f3ae FREE NOW on Epic Games Store!\n\n"
                "\U0001f4cc " + game["title"] + "\n"
                "\U0001f4c5 Free until " + game["end"] + "\n\n"
                "\U0001f517 " + url
            )
            send_telegram(msg)
            time.sleep(1)
        seen["seen_current"] = list(seen_current | {g["id"] for g in new_current})
    else:
        print("[INFO] No new free games found.")

    # Check for new UPCOMING free games
    new_upcoming = [g for g in upcoming_free if g["id"] not in seen_upcoming]
    if new_upcoming:
        print("[INFO] Found " + str(len(new_upcoming)) + " new UPCOMING free game(s)!")
        for game in new_upcoming:
            url = "https://store.epicgames.com/p/" + game["slug"]
            msg = (
                "\U0001f52e UPCOMING FREE on Epic Games Store!\n\n"
                "\U0001f4cc " + game["title"] + "\n"
                "\U0001f4c5 Free from " + game["start"] + " to " + game["end"] + "\n\n"
                "\U0001f517 " + url
            )
            send_telegram(msg)
            time.sleep(1)
        seen["seen_upcoming"] = list(seen_upcoming | {g["id"] for g in new_upcoming})
    else:
        print("[INFO] No new upcoming free games found.")

    # Save
    save_seen(seen)
    print("[INFO] Tracking " + str(len(seen.get("seen_current", []))) + " current and " + str(len(seen.get("seen_upcoming", []))) + " upcoming free games.")


if __name__ == "__main__":
    main()
