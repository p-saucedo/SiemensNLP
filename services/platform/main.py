from statistics import mean
from typing import List

from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from collections import Counter

from pymongo import UpdateOne

from core_api import get_sentiments, preprocess_corpus, train_tfidf, predict_tfidf
from models.review_instance import raw_data_to_review_instance
from mongo import add_collection, get_all_documents, update_sentiments, get_documents_by_sentiment
from os.path import splitext
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)

#uri = "mongodb+srv://psaucedo:psaucedo@festival.a0vs7hr.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb://mongodb:27017/Siemens"
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)
db = mongo.cx.Siemens


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dataset', methods=["POST"])
def data():
    dataset = []
    collection_name = None

    if request.method == "POST":
        raw_dataset = request.files.get("dataset", [])
        dataset = raw_dataset.read().decode("utf-8").split("\n")
        collection_name, _ = splitext(raw_dataset.filename)

        logger.info(f"Dataset uploaded: {raw_dataset.filename}")

        # Preprocess corpus
        pre = preprocess_corpus(data=dataset)
        logger.info(f"Dataset {collection_name} sent to preprocess")

        # Convert to review instance
        ri_dataset = raw_data_to_review_instance(raw_data=dataset,
                                                 collection_name=collection_name,
                                                 processed_data=pre)
        add_collection(database=db,
                       collection_name=collection_name,
                       documents=[ri.model_dump() for ri in ri_dataset])

        logger.info(f"Dataset {collection_name} uploaded as a new collection")

    return render_template("data.html", dataset=dataset, len_dataset=len(dataset), collection_name=collection_name)


@app.route('/sentiments', methods=["POST"])
def sentiments():
    collection_name = request.form.get("collectionName", "col1")

    logger.info(f"Retrieving data from {collection_name} collection...")

    dataset = get_all_documents(database=db, collection_name=collection_name)

    processed_text = [d.get("processed_text") for d in dataset]

    raw_data = [d.get("raw_text") for d in dataset]

    logger.info(f"Sending collection {collection_name} to sentiments detection")

    sents = get_sentiments(data=processed_text)

    logger.info(f"Updating collection {collection_name} with sentiments information")

    ret = update_sentiments(
        database=db,
        collection_name=collection_name,
        documents=dataset,
        sentiments=sents
    )

    return render_template("sentiments.html",
                           sentiments_dataset=zip(raw_data, sents),
                           len_dataset=len(raw_data),
                           sentiments_count=count_sentiments(sns=sents),
                           mean_sentiment=round(mean(sents), 2),
                           collection_name=collection_name)


def count_sentiments(sns: List[int]):
    counter = Counter(sns)

    return list({k: counter.get(k, 0) for k in range(1, 6)}.values())


@app.route('/tfidf', methods=["POST"])
def tfidf():
    collection_name = request.form.get("collectionName", "col1")

    logger.info(f"Retrieving data from {collection_name} collection...")

    dataset = get_all_documents(database=db, collection_name=collection_name)

    processed_text = [d.get("processed_text") for d in dataset]

    train_tfidf(data=processed_text)

    results = {}
    for i in range(1, 6):
        doc_subset = get_documents_by_sentiment(database=db,
                                                collection_name=collection_name,
                                                sentiment_min=i)
        ret = predict_tfidf(data=[doc.get("processed_text") for doc in doc_subset])
        results[i] = list(ret.keys())[:10]

    return render_template("tfidf.html",
                           tfidf_values=results,
                           collection_name=collection_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
