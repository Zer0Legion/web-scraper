from openai import OpenAI
from dotenv import dotenv_values
import requests

CONFIG = {
    **dotenv_values("./.env")
}
URL = "https://api.openai.com/v1/chat/completions"

PROMPT = """
I have scraped several Google News articles related to the stock {}. Please provide the following:

1. A concise summary of the 3 main key points from these news articles. Prefix this with a '###' header, named "Summary:".
2. An analysis of the sentiment (ecstatic, positive, neutral, negative, disastrous) of the articles based on how they affect the stock's outlook. Prefix this with a '###' header, named "Sentiment Analysis: <Your evaluation>".
{}
"""

class Prompter:


    def __init__(self):
        self.cache = {}
        self.client = OpenAI(organization="Personal", project="Default project", api_key=CONFIG["OPENAI_API_KEY"])

    def generate_written_prompt(self, stock, formatted_html):
        """
        Generate a written prompt for the stock based on the formatted HTML.
        """
        if stock in self.cache:
            return self.cache[stock]
        else:
            text = PROMPT.format(stock, formatted_html)
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + CONFIG["OPENAI_API_KEY"]
            }
            data = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": text}],
                "temperature": 0.7
            }

            response = requests.post(URL, headers=headers, json=data).json()
            self.cache[stock] = response
            return response

    def generate_image_prompt(self, text_prompt, sentiment):
        """
        Generate an image prompt based on the text prompt.
        """

        TEMPLATE = """
        Generate an image based on the following text prompt. You may show an office setting of the company that I am mentioning. 
        If you are about to generate an image of a person, I would prefer you to generate an executive in smartly dressed attire, 
        of different genders and races. 
        
        If possible, you are allowed to show the company logo. However, do not generate any text or numbers.

        {}

        I would prefer the picture to show a verb, such as "presenting an earnings report" or "celebrating a successful quarter".

        I want to reflect the sentiment of the news articles in the image. The sentiment is {}.
        """

        prompt = TEMPLATE.format(text_prompt, sentiment)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + CONFIG["OPENAI_API_KEY"]
        }

        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1
        }

        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data).json()
        print(response)
        image_url = response["data"][0]["url"]
        return image_url
    
if __name__ == "__main__":
    prompter = Prompter()

    # Positive
    # print(prompter.generate_image_prompt("Sales and Stock Performance: Apple COO Jeffrey Williams sold $24.9 million in stock, while analysts are optimistic about the company's future, with some firms raising their price targets and maintaining buy ratings amid a solid earnings report.", "Positive"))

    # Disastrous
    # print(prompter.generate_image_prompt("On September 15, 2008, Lehman Brothers filed for Chapter 11 bankruptcy protection following the exodus of most of its clients, drastic declines in its stock price, and the devaluation of assets by credit rating agencies. The collapse was largely due to Lehman's involvement in the subprime mortgage crisis and its exposure to less liquid assets.[6][7][8] Lehman's bankruptcy filing was the largest in US history, beating the previous record holder Enron,[9] and is thought to have played a major role in the unfolding of the 2007-2008 financial crisis. The market collapse also gave support to the 'too big to fail' doctrine.[10]", "Disastrous"))

    # Slightly negative
    # print(prompter.generate_image_prompt("After trading higher for much of the day, the S&P 500 changed course following the rate-cut announcement and as Fed Chair Jerome Powell addressed the press, ending with a daily loss of 3%. The Dow finished the session down 2.6%, extending its streak of down days to double digits for the first time in four decades. The Nasdaq dropped 3.6% as concerns about the interest-rate outlook weighed on the tech sector.", "Slightly negative"))