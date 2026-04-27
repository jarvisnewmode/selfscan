def calculate_risk(username_results, email_result=None, phone_result=None):
    score = 0
    max_score = 10

    # Username exposure
    if username_results:
        found_count = sum(1 for v in username_results.values() if v["found"])
        score += found_count

    # Email breach
    if email_result and email_result.get("valid_format"):
        score += 1

    # Phone valid
    if phone_result and phone_result.get("valid"):
        score += 1

    # Risk percentage
    percentage = min(int((score / max_score) * 100), 100)

    if percentage < 30:
        level = "Low"
    elif percentage < 70:
        level = "Medium"
    else:
        level = "High"

    return {
        "level": level,
        "percentage": percentage
    }