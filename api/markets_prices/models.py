from pydantic import BaseModel
from datetime import date

class HistoryRequest(BaseModel):
    ids:int|list[int]
    date_from: str
    date_to: str

