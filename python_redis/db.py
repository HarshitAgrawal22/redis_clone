from pymongo import MongoClient


client = MongoClient("mongodb://127.0.0.1:27017/")


class Database:
    def __init__(self, db_name):
        self.db = client[db_name]
        # collection.insert_one({"init": True})
        # print("Inserted into:", Conn)
        self.collection = None

    @staticmethod
    def new_db(db_name: str):
        return Database(db_name)

    def new_connection(self, Conn: str):
        self.collection = self.db[Conn]
        return self.collection

    def new_collection(self, name):
        c = self.db[name]
        # collection.insert_one(
        #     {
        #         "name": "Harsh",
        #         "project": "Redis Clone",
        #         "features": ["list", "set", "graph", "queue"],
        #     }
        # )
        # Insert a single document
        data = {
            "name": "Harsh",
            "project": "Redis Clone",
            "features": ["list", "set", "graph", "queue"],
        }
        insert_result = c.insert_one(data)
        print(f"Inserted document with _id: {insert_result.inserted_id}")

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
