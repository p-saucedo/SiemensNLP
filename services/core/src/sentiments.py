from statistics import mean
from typing import List, Dict, Union

from transformers import pipeline

from src.models import InputText
import re

sentiment_pipeline = pipeline("sentiment-analysis",
                              model="nlptown/bert-base-multilingual-uncased-sentiment",
                              device="cpu")


def get_number_of_stars(label: str) -> int:
    return int(re.findall(r'\d+', label)[0])

def get_sentiments(input_data: List[InputText]) -> List[int]:
    sentiments = []
    for i_data in input_data:
        i_data_len = len(i_data.text)

        if i_data_len > 512:
            chunks = [i_data.text.lower()[i:i + 512] for i in range(0, i_data_len, 512)]
            rets = sentiment_pipeline(chunks)
            sentiments.append(round(mean([get_number_of_stars(label=ret.get("label", "1 stars")) for ret in rets])))
        else:
            sentiments.append(get_number_of_stars(label=sentiment_pipeline(i_data.text)[0].get("label", "1 stars")))
    return sentiments

