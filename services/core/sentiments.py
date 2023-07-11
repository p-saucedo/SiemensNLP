from typing import List, Dict, Union

from transformers import pipeline

from models import InputText

sentiment_pipeline = pipeline("sentiment-analysis",
                              model="nlptown/bert-base-multilingual-uncased-sentiment",
                              device="cpu")


def get_sentiments(input_data: List[InputText]) -> List[Dict[str, Union[str, float]]]:
    return sentiment_pipeline([i_data.text for i_data in input_data])
