import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import dotenv_values

import markdown

CONFIG = {**dotenv_values("./.env")}


def send_email(to_email, subject, body):
    # Email credentials
    from_email = CONFIG["EMAIL_ADDRESS"]
    password = CONFIG["EMAIL_PASSWORD"]

    # Convert Markdown to HTML
    html_body = markdown.markdown(body)

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    # Connect to the Gmail SMTP server
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()

    # Log in to the server
    server.login(from_email, password)

    # Send the email
    server.sendmail(from_email, to_email, msg.as_string())

    # Close the connection
    server.quit()

    print("Email sent successfully!")


if __name__ == "__main__":
    send_email(
        "lengkhai@gmail.com",
        "test subject",
        "###header\r\nThis is a **test** email with _Markdown_ content.",
    )
