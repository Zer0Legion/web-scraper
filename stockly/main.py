import requests
import yfinance as yf

from Email import EmailService
from Parser import ParserService
from ProjectIo import ProjectIoService
from Prompter import PrompterService

URL = "https://www.google.com/finance/quote/"
URL_NEWS = "https://news.google.com/search?q="


def main(input_dict):
    io = ProjectIoService()
    prompter = PrompterService()
    parser = ParserService()
    email_service = EmailService()

    db = io.load_db(input_dict)

    for email in db:
        stocks = db[email]["stocks"]
        io.generate_intro(db[email]["name"])

        for exchange in stocks:
            for stock in stocks[exchange]:
                # Get the long name of the stock
                exchange_name = f"{exchange}:{stock}"
                long_name = yf.Ticker(stock).info["longName"]

                io.add_next_stock(long_name, exchange_name)

                # Clean and parse the news articles
                html_response = requests.get(URL_NEWS + exchange_name).text
                cleaned_html = parser.format_html(
                    exchange_name, long_name, html_response
                )

                # Generate and send the prompt
                chatgpt_response = prompter.generate_written_prompt(stock, cleaned_html)
                chatgpt_text = chatgpt_response["choices"][0]["message"]["content"]

                io.append_report(chatgpt_text + "\n\n")

        # Send the email
        email_service.send_email(email, io.content)


if __name__ == "__main__":
    main("./stockly/in/test_db.json")
