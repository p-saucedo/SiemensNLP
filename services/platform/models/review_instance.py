from typing import List

from pydantic import BaseModel


class ReviewInstance(BaseModel):
    id: str
    raw_text: str
    processed_text: str
    sentiment: float
    topics: List[str]