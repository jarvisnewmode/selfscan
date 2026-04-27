from flask import Flask, render_template, request, redirect, url_for
from scanners.username_scanner import scan_username
from scanners.phone_scanner import analyze_phone
from scanners.email_scanner import analyze_email
from scanners.risk_engine import calculate_risk

app = Flask(__name__)

feedback_list = []


@app.errorhandler(500)
def internal_error(error):
    return render_template("error.html"), 500


@app.route("/", methods=["GET", "POST"])
def home():

    username_data = None
    phone_result = None
    email_result = None
    risk_data = None

    if request.method == "POST":

        username = request.form.get("username")
        phone = request.form.get("phone")
        email = request.form.get("email")

        if username and username.strip():
            username_data = scan_username(username)

        if phone and phone.strip():
            phone_result = analyze_phone(phone)

        if email and email.strip():
            email_result = analyze_email(email)

        risk_data = calculate_risk(
            username_data["verified"] if username_data else None,
            email_result,
            phone_result
        )

    average_rating = None
    if feedback_list:
        average_rating = round(
            sum(item["rating"] for item in feedback_list) / len(feedback_list),
            1
        )

    return render_template(
        "index.html",
        username_data=username_data,
        phone_result=phone_result,
        email_result=email_result,
        risk_data=risk_data,
        feedback_list=feedback_list,
        average_rating=average_rating
    )


@app.route("/feedback", methods=["POST"])
def feedback():

    rating = request.form.get("rating")
    comment = request.form.get("comment")

    if rating:
        feedback_list.append({
            "rating": int(rating),
            "comment": comment
        })

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()