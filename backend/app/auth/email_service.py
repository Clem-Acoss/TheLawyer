import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")

def send_email(to_email: str, subject: str, html_content: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM
        msg["To"] = to_email

        # Ajoute le contenu HTML
        part = MIMEText(html_content, "html", "utf-8")
        msg.attach(part)

        # Connexion SMTP avec TLS
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
           server.starttls()
           server.login(SMTP_USER, SMTP_PASSWORD)
           server.sendmail(SMTP_FROM, to_email, msg.as_string())

        logging.info(f"[EMAIL] Email envoyé à {to_email}")

    except Exception as e:
        logging.error(f"[EMAIL] Erreur lors de l'envoi du mail à {to_email} : {e}")
        raise
