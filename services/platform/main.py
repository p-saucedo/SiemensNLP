from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)

uri = "mongodb+srv://psaucedo:psaucedo@festival.a0vs7hr.mongodb.net/?retryWrites=true&w=majority"

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/Siemens"
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dataset', methods=["POST"])
def data():
    dataset = []
    if request.method == "POST":
        raw_dataset = request.files.get("dataset", [])
        dataset = raw_dataset.read().decode("utf-8").split("\n")

    return render_template("data.html", dataset=dataset)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
