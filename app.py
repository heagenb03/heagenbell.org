import os
import resend
from flask import Flask, render_template, redirect, request

app = Flask(__name__,template_folder='./templates', static_folder='./static')

resend.api_key = os.environ["RESEND_API_KEY"]
ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
CONTACT_EMAIL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Message Notification</title>
</head>
<body>
    <h2>New Message Received!</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong></p>
    <blockquote>
        {message}
    </blockquote>
</body>
</html>
"""

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Load form data
        form_data = request.form.to_dict()

        # Configuring the email fields
        params = {
            "from": "Your Flask App <delivered@resend.dev>",
            "to": [ADMIN_EMAIL],
            "subject": f"New message from {form_data['name']}!",
            "html": CONTACT_EMAIL.format(**form_data),
        }

        # Sending the email and catching response
        response = resend.Emails.send(params)

        # Handle the response
        if response.get("id"):
            return redirect("/contact")
        else:
            return {"message": "Something went wrong. Please try again."}
    else:
        # Render the contact form
        return render_template("index.html")
