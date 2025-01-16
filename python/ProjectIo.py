# Class to handle input/output operations

import os
import json
from dotenv import dotenv_values

CONFIG = {
    **dotenv_values("./.env")
}

CONTENT_PREFIX = "Dear {},\n\nGood morning from all of us at {}! Here is our curated summary for you:\n\n# Report of your selected stocks:\n\n"

class ProjectIo:

    content = ""
    stocks = {}
    db = {}

    def __init__(self):
        pass
        
    def load_stocks(self, filename):
        with open(filename, 'r') as f:
            self.stocks = json.load(f)
            return self.stocks

    def load_db(self, filename):
        with open(filename, 'r') as f:
            self.db = json.load(f)
            return self.db
        
    def generate_intro(self, user_email):
        try:
            self.content = CONTENT_PREFIX.format(self.db[user_email], CONFIG["ORG_NAME"])
        except:
            self.content = CONTENT_PREFIX.format(user_email, CONFIG["ORG_NAME"])
    
    def add_next_stock(self, long_name, exchange_name):
        self.content += f"## {long_name} ({exchange_name})\n\n"
    
    def print_report(self, data): 
        self.content += data

    def append_report(self, data):
        self.content += data
    
    def write_to_file(self, filename, data):
        self.make_file(filename)
        with open(filename, 'w', encoding="utf=8") as f:
            f.write(data)
    
    def append_to_file(self, filename, data):
        self.make_file(filename)
        with open(filename, 'a', encoding="utf=8") as f:
            f.write(data)
    
    def make_file(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)