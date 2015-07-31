import json

def insert_data(data, db):
    db.arachnid.insert(data)



if __name__ == "__main__":

    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    with open('arachnid.json') as f:
        data = json.loads(f.read())
        print(db.collection_names(include_system_collections=False))
        insert_data(data, db)
        print(db.arachnid.find_one())
