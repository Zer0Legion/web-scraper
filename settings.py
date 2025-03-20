from dotenv import dotenv_values
from pydantic import BaseModel


class Settings(BaseModel):
    ORG_NAME: str = "Stockly"

    # Sending emails
    EMAIL_ADDRESS: str = "EMAIL_ADDRESS"
    EMAIL_PASSWORD: str = "EMAIL_PASSWORD"

    # OpenAI
    OPENAI_API_KEY: str = "OPENAI_API_KEY"

    # Instagram
    INSTA_USER_ID: str = "user"
    INSTA_ACCESS_TOKEN: str = "token"

    URL_NEWS: str = "https://news.google.com/search?q="

    def get_settings(self) -> "Settings":
        config = {**dotenv_values("./.env")}
        for key, value in config.items():
            setattr(self, key, value)
        return self
