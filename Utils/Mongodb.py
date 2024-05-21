from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri, db_name='test'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_one(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def insert_many(self, collection_name, documents):
        collection = self.db[collection_name]
        result = collection.insert_many(documents)
        return result.inserted_ids

    def find_one(self, collection_name, query):
        collection = self.db[collection_name]
        document = collection.find_one(query)
        return document

    def find_many(self, collection_name, query):
        collection = self.db[collection_name]
        documents = collection.find(query)
        return list(documents)

    def update_one(self, collection_name, query, update):
        collection = self.db[collection_name]
        result = collection.update_one(query, {'$set': update})
        return result.modified_count

    def update_many(self, collection_name, query, update):
        collection = self.db[collection_name]
        result = collection.update_many(query, {'$set': update})
        return result.modified_count

    def delete_one(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count

    def delete_many(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_many(query)
        return result.deleted_count

    def close(self):
        self.client.close()