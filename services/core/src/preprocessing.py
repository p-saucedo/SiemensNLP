from typing import List

import nltk
from nltk import word_tokenize
from string import punctuation

from nltk.corpus import stopwords
from tokenizers import Tokenizer

from src.models import InputText
from src.sentiments import get_sentiments
import re

NLTK_DATA_PATH = "./nltk_data"
nltk.download('stopwords', download_dir=NLTK_DATA_PATH)
nltk.download('punkt', download_dir=NLTK_DATA_PATH)
nltk.data.path.append(NLTK_DATA_PATH)

stop_words = stopwords.words('english')
stemmer = nltk.PorterStemmer()


def preprocess_data(input_data: List[InputText]) -> List[str]:
    return [" ".join(tokenize(
                    remove_stopwords(
                        clean_text(d.text)
                    )

    )) for d in input_data]


def clean_text(data: str) -> str:
    text = str(data).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


def tokenize(data: str) -> List[str]:
    tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
    inputs = tokenizer.encode(data)
    return inputs.tokens[1:-1]


"""def stemm_text(data: str) -> str:
    text = ' '.join(stemmer.stem(word) for word in data.split(' '))
    print(text)
    return text"""


def remove_stopwords(data: str) -> str:
    return ' '.join(word for word in data.split(' ') if word not in stop_words)

if __name__ == '__main__':
    ret = preprocess_data(input_data=[InputText(text="Replace by any text you'd like.")])
    print(ret)