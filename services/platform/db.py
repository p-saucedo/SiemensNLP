from flask_pymongo import PyMongo

mongo = PyMongo(app)
db = mongo.cx.Siemens
