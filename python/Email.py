import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
from datetime import date

from dotenv import dotenv_values


CONFIG = {
    **dotenv_values("./.env")
}

SUBJECT = "[{}] Your {} Stock Briefing"

class Email:
    def send_email(to_email, body):
        # Email credentials
        from_email = CONFIG["EMAIL_ADDRESS"]
        password = CONFIG["EMAIL_PASSWORD"]

        # Convert Markdown to HTML
        html_body = markdown.markdown(body)

        todays_date = date.today().strftime("%b %d")

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = SUBJECT.format(CONFIG["ORG_NAME"], todays_date)
        msg.attach(MIMEText(html_body, 'html'))

        # Connect to the Gmail SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()

        # Log in to the server
        server.login(from_email, password)

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())

        # Close the connection
        server.quit()
