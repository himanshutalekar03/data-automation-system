import smtplib
from email.message import EmailMessage


def send_email(receiver_email, message_text):

    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"

    msg = EmailMessage()
    msg.set_content(message_text)
    msg["Subject"] = "Business Data Processing Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)
