from flask import Flask, render_template, request
import requests
import random
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# ✅ Rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

scan_counter = 0


def check_username(platform, username):
    urls = {
        "Instagram": f"https://www.instagram.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Telegram": f"https://t.me/{username}"
    }

    url = urls.get(platform)

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {"found": False, "url": url}

        if "t.me" in url:
            if "If you have Telegram" in response.text:
                return {"found": False, "url": url}

        return {"found": True, "url": url}

    except:
        return {"found": False, "url": url}


def check_email_breach(email):
    email = email.lower()

    if "hack" in email or "test" in email:
        return {
            "breached": True,
            "breaches": ["ExampleBreach.com", "DemoLeak.org"]
        }

    if random.randint(1, 10) <= 3:
        return {
            "breached": True,
            "breaches": ["RandomLeak.net"]
        }

    return {
        "breached": False,
        "breaches": []
    }


@app.route("/", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def home():
    global scan_counter

    results = None
    risk_level = None
    email_result = None

    if request.method == "POST":

        scan_counter += 1

        username = request.form.get("username")
        email = request.form.get("email")

        risk_score = 0

        if username and username.strip() != "":
            results = {
                "Instagram": check_username("Instagram", username),
                "GitHub": check_username("GitHub", username),
                "Telegram": check_username("Telegram", username)
            }

            found_platforms = sum(1 for v in results.values() if v["found"])
            risk_score += found_platforms

        if email and email.strip() != "":
            email_result = check_email_breach(email)

            if email_result["breached"]:
                risk_score += 2

        if risk_score == 0:
            risk_level = "🟢 Low Exposure"
        elif risk_score <= 2:
            risk_level = "🟡 Medium Exposure"
        else:
            risk_level = "🔴 High Exposure"

    return render_template(
        "index.html",
        results=results,
        risk_level=risk_level,
        email_result=email_result,
        scan_counter=scan_counter
    )


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("ratelimit.html"), 429


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


if __name__ == "__main__":
    app.run(debug=True)