from h11 import Response
import requests
import yfinance as yf
from fastapi import Depends, FastAPI, responses

from backend.dependencies.base import (
    get_email_service,
    get_parser_service,
    get_project_io_service,
    get_prompter_service,
)
from backend.errors.base import StocklyError
from objects.api.response import ErrorResponse, SuccessResponse

from objects.requests.send_briefing_email import SendEmailRequest
from backend.services.Email import EmailService
from backend.services.Parser import ParserService
from backend.services.ProjectIo import ProjectIoService
from backend.services.openai.Prompter import PrompterService

URL = "https://www.google.com/finance/quote/"
URL_NEWS = "https://news.google.com/search?q="

app = FastAPI()


@app.get("/")
def home():
    """
    Default landing page for API.

    Returns
    -------
    SuccessResponse[str]
        hello world string.
    """
    return SuccessResponse(data="Stockly API is running.")


@app.post(
    path="/send_email",
    dependencies=[
        Depends(get_email_service),
        Depends(get_parser_service),
        Depends(get_project_io_service),
        Depends(get_prompter_service),
    ],
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
    },
)
def send_email(
    param: SendEmailRequest,
    email_service: EmailService = Depends(get_email_service),
    parser_service: ParserService = Depends(get_parser_service),
    project_io_service: ProjectIoService = Depends(get_project_io_service),
    prompter_service: PrompterService = Depends(get_prompter_service),
):
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
                stock_info = yf.Ticker(stock.ticker)
                long_name = stock_info.info["longName"]

                project_io_service.add_next_stock(long_name, stock.full_name)

                html_response = requests.get(URL_NEWS + stock.full_name).text
                cleaned_html = parser_service.format_html(
                    stock.full_name, long_name, html_response
                )

                chatgpt_response = prompter_service.generate_written_prompt(
                    stock.ticker, cleaned_html
                )
                chatgpt_text = chatgpt_response["choices"][0]["message"]["content"]

                project_io_service.append_report(chatgpt_text + "\n\n")

            email_service.send_email(request.email, project_io_service.content)

        return SuccessResponse(data="Email sent successfully.")
    except StocklyError as e:
        return ErrorResponse(
            error_code=e.error_code,
            error_message=str(e)
        )

