# Class to handle input/output operations

import os
import json
from dotenv import dotenv_values
import requests

from objects.requests.stock import StockRequestInfo

from ..errors.env import EnvironmentVariableNotSuppliedError


class ProjectIoService:
    def __init__(self):
        self.CONTENT_PREFIX = "Dear {},\n\nGood morning from all of us at {}! Here is our curated summary for you:\n\n# Report of your selected stocks:\n\n"
        CONFIG = {**dotenv_values("./.env")}
        if not CONFIG["ORG_NAME"]:
            raise EnvironmentVariableNotSuppliedError(["organization name"])
        self.db = {}
        self.stocks = {}
        self.content = ""

        self.org_name = CONFIG["ORG_NAME"]

    def load_stocks(self, filename: os.PathLike) -> dict:
        with open(filename, "r") as f:
            self.stocks = json.load(f)
            return self.stocks

    def load_db(self, filename: os.PathLike):
        with open(filename, "r") as f:
            self.db = json.load(f)
            return self.db

    def generate_intro(self, user_email: str):
        org_name: str = self.org_name

        if user_email in self.db:
            self.content = self.CONTENT_PREFIX.format(self.db[user_email], org_name)
        else:
            self.content = self.CONTENT_PREFIX.format(user_email, org_name)

    def add_next_stock(self, stock: StockRequestInfo):
        self.content += f"## {stock.long_name} ({stock.ticker})\n\n"

    def print_report(self, data: str):
        self.content += data

    def append_report(self, data: str):
        self.content += data

    def write_to_file(self, filename: os.PathLike, data: str):
        self.make_file(filename)
        with open(filename, "w", encoding="utf=8") as f:
            f.write(data)

    def append_to_file(self, filename: os.PathLike, data: str):
        self.make_file(filename)
        with open(filename, "a", encoding="utf=8") as f:
            f.write(data)

    def make_file(self, filename: os.PathLike):
        """
        Make a file with the given filename if it does not exist.

        Parameters
        ----------
        filename : os.PathLike
            filename
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def download_image(self, image_url: str, filename: str = "filename.jpg") -> str:
        """
        Downloads an image from the given URL.

        Parameters
        ----------
        image_url : str
            url of the image
        filename : str, optional
            file name, by default "filename"
        
        Returns
        -------
        str
            filename
        """
        img_data = requests.get(image_url).content

        with open("filename", "wb") as handler:
            handler.write(img_data)
        
        return filename
    
