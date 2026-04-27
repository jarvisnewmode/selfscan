import re


def analyze_phone(phone):
    phone = phone.strip()

    result = {
        "valid": False,
        "country": "Unknown",
        "carrier": "Unknown (Demo)",
        "line_type": "Unknown"
    }

    # Oddiy validatsiya (9–15 ta raqam, + bilan boshlanishi mumkin)
    pattern = r"^\+?\d{9,15}$"

    if re.match(pattern, phone):
        result["valid"] = True

        # Demo country detection
        if phone.startswith("+998"):
            result["country"] = "Uzbekistan"
            result["line_type"] = "Mobile"

        elif phone.startswith("+1"):
            result["country"] = "USA"
            result["line_type"] = "Mobile"

        elif phone.startswith("+44"):
            result["country"] = "United Kingdom"
            result["line_type"] = "Mobile"

        else:
            result["country"] = "International"

    return result