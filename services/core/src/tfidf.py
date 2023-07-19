from typing import List
from joblib import dump, load
import pandas as pd
from os.path import join
from sklearn.feature_extraction.text import TfidfVectorizer

from src.models import InputText


def train_tfidf(corpus: List[InputText], output_dir: str = "./src/data") -> str:
    tfidf = TfidfVectorizer(use_idf=True).fit([c.text for c in corpus])
    output_path = join(output_dir, "tfidf.joblib")
    dump(tfidf, output_path)
    return "OK"


def predict_tfidf(corpus: List[InputText], tfidf_path: str = join("./src/data", "tfidf.joblib")):
    tfidf = load(filename=tfidf_path)

    tfidf_matrix = tfidf.transform([c.text for c in corpus])
    results = pd.DataFrame(tfidf_matrix.sum(axis=0).T, index=tfidf.get_feature_names_out(), columns=["tfidf"])
    return results.sort_values(by=["tfidf"], ascending=False)["tfidf"]
