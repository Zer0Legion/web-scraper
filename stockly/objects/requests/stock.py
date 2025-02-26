from pydantic import BaseModel

import yfinance as yf

class StockRequestInfo(BaseModel):
    exchange: str
    ticker: str

    @property
    def full_name(self):
        return f"{self.exchange}:{self.ticker}"

    @property
    def long_name(self) -> str:
        """Return long name of stock."""
        
        return yf.Ticker(self.ticker).info["longName"]