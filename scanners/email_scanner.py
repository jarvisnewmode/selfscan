import re
import dns.resolver

DISPOSABLE_DOMAINS = [
    "mailinator.com",
    "10minutemail.com",
    "tempmail.com"
]


def analyze_email(email):
    email = email.strip().lower()

    result = {
        "valid_format": False,
        "domain": None,
        "mx_record": False,
        "disposable": False
    }

    # Format check
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if re.match(pattern, email):
        result["valid_format"] = True
        domain = email.split("@")[1]
        result["domain"] = domain

        # Disposable check
        if domain in DISPOSABLE_DOMAINS:
            result["disposable"] = True

        # MX record check
        try:
            dns.resolver.resolve(domain, "MX")
            result["mx_record"] = True
        except:
            result["mx_record"] = False

    return result