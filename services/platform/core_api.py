from typing import List

import requests

CORE_API_PATH = "http://127.0.0.1:8081"


def get_sentiments(data: List[str]):
    url = f"{CORE_API_PATH}/sentiment"
    ret = requests.post(url, json=[{"text": txt} for txt in data])
    return ret.json()


def preprocess_corpus(data: List[str]):
    url = f"{CORE_API_PATH}/preprocess"
    ret = requests.post(url, json=[{"text": txt} for txt in data])
    return ret.json()
