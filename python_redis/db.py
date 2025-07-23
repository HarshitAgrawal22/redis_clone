from pymongo import MongoClient


client = MongoClient("mongodb://127.0.0.1:27017/")


class Database:
    def __init__(self, db_name):
        self.db = client[db_name]

    @staticmethod
    def new_db(db_name: str):
        return Database(db_name)

    def new_connection(self, Conn: str):
        self.collection = self.db[Conn]
        return self.collection

    def new_collection(self, name):
        collection = self.db[name]

        data = {
            "name": "Harshit",
            "project": "Redis Clone",
            "features": ["list", "set", "graph", "queue"],
        }
        insert_result = collection.insert_one(data)
        print(f"Inserted document with _id: {insert_result.inserted_id}")

    def insert_element(self, name, item):
        collection = self.db[name]

        insert_result = collection.insert_one(item)
        print(f"Inserted document with _id: {insert_result.inserted_id}")
        return "yes"

    @staticmethod
    def drop_peer_db(Conn):
        client.drop_database(Conn)


# # Insert One
# collection.insert_one({"name": "Alice", "age": 25})

# # Insert Many
# collection.insert_many([{"name": "Bob"}, {"name": "Charlie"}])

# # Find
# result = collection.find_one({"name": "Alice"})
# print(result)

# # Update
# collection.update_one({"name": "Alice"}, {"$set": {"age": 26}})

# # Delete
# collection.delete_one({"name": "Bob"})
