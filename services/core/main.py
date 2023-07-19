from typing import List

from fastapi import FastAPI
import uvicorn

from src.models import InputText
from src.preprocessing import preprocess_data
from src.sentiments import get_sentiments
from src.tfidf import train_tfidf, predict_tfidf

app = FastAPI()


@app.post("/sentiment")
async def extract_sentiments(input_data: List[InputText]):
    return get_sentiments(input_data=input_data)


@app.post("/preprocess")
async def preprocess(input_data: List[InputText]):
    return preprocess_data(input_data=input_data)


@app.post("/tfidffit")
async def tfidf_train(input_data: List[InputText]):
    return train_tfidf(corpus=input_data)


@app.post("/tfidfpredict")
async def tfidf_predict(input_data: List[InputText]):
    return predict_tfidf(corpus=input_data)


@app.post("/health")
async def health():
    return "OK"


if __name__ == '__main__':
    from uvicorn_config import config

    uvicorn.run("main:app", port=8081, host='127.0.0.1', reload=True, **config)
