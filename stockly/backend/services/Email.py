import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
from datetime import date

from dotenv import dotenv_values

from ..errors.env import (
    CredentialsNotSuppliedError,
    EnvironmentVariableNotSuppliedError,
)


class EmailService:
    def __init__(self):
        CONFIG = {**dotenv_values("./.env")}
        self.SUBJECT = "[{}] Your {} Stock Briefing"

        if not CONFIG["ORG_NAME"]:
            raise EnvironmentVariableNotSuppliedError(["organization name"])
        if not CONFIG["EMAIL_ADDRESS"]:
            raise CredentialsNotSuppliedError(["sender email address"])
        if not CONFIG["EMAIL_PASSWORD"]:
            raise CredentialsNotSuppliedError(["sender email password"])

        self.org_name = CONFIG["ORG_NAME"]
        self.from_email: str = CONFIG["EMAIL_ADDRESS"]
        self.password: str = CONFIG["EMAIL_PASSWORD"]

    def send_email(self, to_email: str, body: str):
        # Convert Markdown to HTML
        html_body = markdown.markdown(body)

        todays_date = date.today().strftime("%b %d")

        # Create the email message
        message_body = MIMEMultipart()
        message_body["From"] = self.from_email
        message_body["To"] = to_email
        message_body["Subject"] = self.SUBJECT.format(self.org_name, todays_date)
        message_body.attach(MIMEText(html_body, "html"))

        # Connect to the Gmail SMTP server
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()

        # Log in to the server
        server.login(self.from_email, self.password)

        # Send the email
        server.sendmail(self.from_email, to_email, message_body.as_string())

        # Close the connection
        server.quit()
