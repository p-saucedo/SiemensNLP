from flask import Flask, render_template, request
from flask_pymongo import PyMongo

from core_api import get_sentiments
from models.review_instance import raw_data_to_review_instance
from mongo import add_collection, get_all_documents
from os.path import splitext

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

        # Convert to review instance
        ri_dataset = raw_data_to_review_instance(raw_data=dataset, collection_name=collection_name)
        add_collection(database=db,
                       collection_name=collection_name,
                       documents=[ri.model_dump() for ri in ri_dataset])

    return render_template("data.html", dataset=dataset, len_dataset=len(dataset), collection_name=collection_name)


@app.route('/sentiments', methods=["POST"])
def sentiments():
    collection_name = request.form.get("collectionName", "col1")
    dataset = get_all_documents(database=db, collection_name=collection_name)
    raw_data = [d.get("raw_text") for d in dataset]
    sentiments = [round(s.get("score"), 3) for s in get_sentiments(data=raw_data)]
    return render_template("sentiments.html", sentiments_dataset=zip(raw_data, sentiments), len_dataset=len(raw_data))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
