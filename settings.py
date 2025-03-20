from dotenv import dotenv_values
from pydantic import BaseModel


class Settings(BaseModel):
    ORG_NAME: str = "Stockly"

    # Sending emails
    EMAIL_ADDRESS: str = "EMAIL_ADDRESS"
    EMAIL_PASSWORD: str = "EMAIL_PASSWORD"

    # Briefing email
    CONTENT_PREFIX: str = "Dear {},\n\nGood morning from all of us at {}! Here is our curated summary for you:\n\n# Report of your selected stocks:\n\n"

    # OpenAI
    OPENAI_API_KEY: str = "OPENAI_API_KEY"
    OPENAI_URL: str = "https://api.openai.com/v1/chat/completions"

    # Instagram
    INSTA_USER_ID: str = "user"
    INSTA_ACCESS_TOKEN: str = "token"

    URL_NEWS: str = "https://news.google.com/search?q="

    def get_settings(self) -> "Settings":
        config = {**dotenv_values("./.env")}
        for key, value in config.items():
            setattr(self, key, value)
        return self
