from flask import Flask, render_template, request, jsonify
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Config - cambiar con datos reales si se desea email
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
TO_EMAIL = os.environ.get("TO_EMAIL", "franbure0510@gmail.com")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    if not all([name, email, subject, message]):
        return jsonify({"error": "All fields are required"}), 400

    if SMTP_USER and SMTP_PASS:
        try:
            msg = MIMEMultipart()
            msg["From"] = SMTP_USER
            msg["To"] = TO_EMAIL
            msg["Subject"] = f"[Portfolio] {subject} - {name}"

            body = f"""
            New message from your portfolio:

            Name: {name}
            Email: {email}
            Subject: {subject}

            Message:
            {message}
            """

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)

            return jsonify({"ok": True, "message": "Message sent successfully"})
        except Exception as e:
            return jsonify({"error": f"Error sending: {str(e)}"}), 500
    else:
        # Development mode: log to console
        print(f"\n{'='*50}")
        print(f"New portfolio message:")
        print(f"  Name: {name}")
        print(f"  Email: {email}")
        print(f"  Subject: {subject}")
        print(f"  Message: {message}")
        print(f"{'='*50}\n")

        return jsonify({
            "ok": True,
            "message": "Message received (development mode)"
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
