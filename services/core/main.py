from typing import List

from fastapi import FastAPI
import uvicorn

from src.models import InputText
from src.preprocessing import preprocess_data
from src.sentiments import get_sentiments

app = FastAPI()


@app.post("/sentiment")
async def extract_sentiments(input_data: List[InputText]):
    return get_sentiments(input_data=input_data)


@app.post("/preprocess")
async def preprocess(input_data: List[InputText]):
    return preprocess_data(input_data=input_data)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8081, host='127.0.0.1', reload=True)
