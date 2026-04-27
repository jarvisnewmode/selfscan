import requests

# ✅ Server tomonidan tekshirish mumkin bo‘lgan platformalar
VERIFIED_PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Keybase": "https://keybase.io/{}",
    "About.me": "https://about.me/{}",
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Steam": "https://steamcommunity.com/id/{}"
}

# ✅ Server tekshira olmaydigan (manual) platformalar
MANUAL_PLATFORMS = {
    "Instagram": "https://www.instagram.com/{}",
    "Telegram": "https://t.me/{}",
    "Twitter": "https://twitter.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}"
}


def check_verified_platform(url):
    """
    Faqat status_code tekshiradi.
    Bu platformalar odatda 404 qaytaradi agar mavjud bo‘lmasa.
    """
    try:
        response = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        return response.status_code == 200

    except:
        return False


def scan_username(username):
    verified_results = {}
    manual_results = {}

    # ✅ VERIFIED scan
    for name, pattern in VERIFIED_PLATFORMS.items():
        url = pattern.format(username)
        found = check_verified_platform(url)

        verified_results[name] = {
            "found": found,
            "url": url
        }

    # ✅ MANUAL scan
    for name, pattern in MANUAL_PLATFORMS.items():
        url = pattern.format(username)

        manual_results[name] = {
            "url": url,
            "note": "Manual verification required (platform blocks automated detection)"
        }

    return {
        "verified": verified_results,
        "manual": manual_results
    }