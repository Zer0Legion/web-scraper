import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
from datetime import date

from dotenv import dotenv_values

from stockly.objects.requests.send_briefing_email import SendEmailRequest

from ..errors.env import (
    CredentialsNotSuppliedError,
    EnvironmentVariableNotSuppliedError,
)


class EmailService:
    def __init__(
            self,
            email_service
parser_service
project_io_service
prompter_service):
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

    def send_briefing_email(self, param: SendEmailRequest):
        """
        Send an email to the user with the stock analysis.

        Parameters
        ----------
        param : SendEmailRequest
            The request object containing the user requests.
        email_service : EmailService
            The email service dependency, auto inject by FastAPI.
        parser_service : ParserService
            The parser service dependency, auto inject by FastAPI.
        project_io_service : ProjectIoService
            The project io service dependency, auto inject by FastAPI.
        prompter_service : PrompterService
            The prompter service dependency, auto inject by FastAPI.

        Returns
        -------
        SuccessResponse[str]
            Email sent successfully.
        """
        try:
            for request in param.user_requests:
                stocks = request.stocks
                project_io_service.generate_intro(request.name)

                for stock in stocks:
                    project_io_service.add_next_stock(stock)

                    html_response = requests.get(URL_NEWS + stock.full_name).text

                    cleaned_html = parser_service.format_html(stock, html_response)

                    chatgpt_response = prompter_service.generate_written_prompt(
                        stock.ticker, cleaned_html
                    )
                    chatgpt_text = chatgpt_response["choices"][0]["message"]["content"]

                    project_io_service.append_report(chatgpt_text + "\n\n")

                email_service.send_email(request.email, project_io_service.content)

            return SuccessResponse(data="Email sent successfully.")
        except StocklyError as e:
            return ErrorResponse(error_code=e.error_code, error_message=str(e))