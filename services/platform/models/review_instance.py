from typing import List
from utils import compute_id
from pydantic import BaseModel


class ReviewInstance(BaseModel):
    _id: str
    raw_text: str
    processed_text: str
    sentiment: float
    topics: List[str]


def raw_data_to_review_instance(raw_data: List[str], collection_name: str) -> List[ReviewInstance]:
    return [ReviewInstance(
        id=compute_id(text=t, collection_name=collection_name),
        raw_text=t,
        processed_text="",
        sentiment=-10,
        topics=[]
    ) for t in raw_data]

