from pymongo import UpdateOne


def add_collection(database, collection_name, documents):
    new_collection = database[collection_name]
    return new_collection.insert_many(documents)


def get_all_documents(database, collection_name):
    collection = database[collection_name]
    return list(collection.find({}))


def update_sentiments(database, collection_name, documents, sentiments):
    mongo_updates = [UpdateOne({"doc_id": d.get("doc_id")}, {"$set": {"sentiment": s}}) for d, s in zip(documents, sentiments)]
    result = database[collection_name].bulk_write(mongo_updates)
    return result
