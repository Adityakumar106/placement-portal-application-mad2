import smtplib
from email.mime.text import MIMEText
from flask import current_app

DEFAULT_SMTP_HOST = "localhost"
DEFAULT_SMTP_PORT = 1025


def init_mail(app):
    app.config.setdefault("SMTP_HOST", DEFAULT_SMTP_HOST)
    app.config.setdefault("SMTP_PORT", DEFAULT_SMTP_PORT)
    app.config.setdefault("SMTP_TIMEOUT", 10)


def send_mail(receiver, subject, body, is_html=False):

    if not receiver:
        raise ValueError("A recipient email address is required")

    msg = MIMEText(
        body,
        "html" if is_html else "plain"
    )

    msg["Subject"] = subject
    msg["From"] = "placementportal@localhost"
    msg["To"] = receiver

    
    host = current_app.config["SMTP_HOST"]
    port = current_app.config["SMTP_PORT"]
    timeout = current_app.config["SMTP_TIMEOUT"]
    with smtplib.SMTP(host, port, timeout=timeout) as server:
        refused = server.sendmail(
            msg["From"],
            [receiver],
            msg.as_string()
        )
        if refused:
            raise smtplib.SMTPRecipientsRefused(refused)

    return True
