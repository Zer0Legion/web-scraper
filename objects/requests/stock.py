from pydantic import BaseModel


class StockRequestInfo(BaseModel):
    exchange: str
    ticker: str

    @property
    def full_name(self):
        return f"{self.exchange}:{self.ticker}"
