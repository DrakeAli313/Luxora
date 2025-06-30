import smtplib
from email.message import EmailMessage
from decouple import config

SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_USERNAME = config("MAILTRAP_USERNAME")  # store in .env
SMTP_PASSWORD = config("MAILTRAP_PASSWORD")

SENDER_EMAIL = "noreply@realestate.com"

def send_listing_email(receiver_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
