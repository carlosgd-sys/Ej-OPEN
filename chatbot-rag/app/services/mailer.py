import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")


def send_email(to_email: str, subject: str, body: str):
    mensaje = MIMEMultipart()
    mensaje["From"] = SMTP_FROM
    mensaje["To"] = to_email
    mensaje["Subject"] = subject

    mensaje.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(mensaje)
            print(f"Email enviado a {to_email}")

    except Exception as e:
        print(f"Error enviando email: {e}")
