from statistics import mean
from typing import List

from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from collections import Counter
from core_api import get_sentiments, preprocess_corpus
from models.review_instance import raw_data_to_review_instance
from mongo import add_collection, get_all_documents
from os.path import splitext
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)

uri = "mongodb+srv://psaucedo:psaucedo@festival.a0vs7hr.mongodb.net/?retryWrites=true&w=majority"
# uri = "mongodb://127.0.0.1:27017/Siemens"
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)
db = mongo.cx.Siemens


@app.route('/')
def index():
    return render_template("index.html", collections=db.list_collection_names())


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

    return render_template("sentiments.html",
                           sentiments_dataset=zip(raw_data, sents),
                           len_dataset=len(raw_data),
                           sentiments_count=count_sentiments(sentiments=sents),
                           mean_sentiment=round(mean(sents),2))


def count_sentiments(sentiments: List[int]):
    cnter = Counter(sentiments)

    return list({k: cnter.get(k, 0) for k in range(1, 6)}.values())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
