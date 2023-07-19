from typing import List, Optional
from utils import compute_id
from pydantic import BaseModel


class ReviewInstance(BaseModel):
    _id: str
    raw_text: str
    processed_text: str
    sentiment: int
    topics: List[str]


def raw_data_to_review_instance(raw_data: List[str],
                                collection_name: str,
                                processed_data: Optional[List[str]]) -> List[ReviewInstance]:
    return [ReviewInstance(
        id=compute_id(text=r, collection_name=collection_name),
        raw_text=r,
        processed_text=p,
        sentiment=-10,
        topics=[]
    ) for r, p in zip(raw_data, processed_data)]

