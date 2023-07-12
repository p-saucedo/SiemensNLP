def add_collection(database, collection_name, documents):
    new_collection = database[collection_name]
    return new_collection.insert_many(documents)

def get_all_documents(database, collection_name):
    collection = database[collection_name]
    return list(collection.find({}))