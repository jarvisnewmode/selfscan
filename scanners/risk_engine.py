def calculate_risk(username_results, email_result=None, phone_result=None):
    score = 0
    max_score = 10

    if username_results:
        found_count = sum(1 for v in username_results.values() if v["found"])
        score += found_count

    if email_result and email_result.get("valid_format"):
        score += 1

    if phone_result and phone_result.get("valid"):
        score += 1

    percentage = min(int((score / max_score) * 100), 100)

    if percentage < 30:
        level = "Low"
        advice = [
            "Your exposure is minimal.",
            "Continue periodic checks.",
            "Use strong and unique passwords."
        ]
    elif percentage < 70:
        level = "Medium"
        advice = [
            "Enable Two-Factor Authentication (2FA).",
            "Review public account visibility settings.",
            "Remove unused public profiles."
        ]
    else:
        level = "High"
        advice = [
            "Immediately review all public accounts.",
            "Enable 2FA everywhere possible.",
            "Consider deleting unused accounts.",
            "Limit public exposure and personal data."
        ]

    return {
        "level": level,
        "percentage": percentage,
        "advice": advice
    }