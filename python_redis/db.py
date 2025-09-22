from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, DeleteResult
from icecream import ic
from pymongo.database import Database

client = MongoClient("mongodb://127.0.0.1:27017/")

from icecream import ic

default_listen_address: str = ":5001"
ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class HardDatabase:
    def __init__(self, db_name):
        self.db: Database = client[db_name]
        # self.collection: Collection = None

    @staticmethod
    def new_db(db_name: str):
        return HardDatabase(db_name)

    def new_collection(self, Conn: str):

        # here we have created a collection
        return self.db[Conn]

    def check_db_existance(self, db_str: str) -> bool:

        return db_str in self.db.list_collection_names()

    def log(self, collection: Collection):
        # ic(self.collection.find())
        ic(collection.find())

    def insert_and_update_element(self, key: str, value: str, collection: Collection):
        try:
            update_result = collection.update_one(
                {"key": key}, {"$set": {"key": key, "value": value}}, upsert=True
            )
            return True
        except Exception as e:
            ic(e)
            return False

    def check_collection_exist(self, collection_name: str) -> bool:
        # return self.db.list_collections(limit=1).alive
        return self.db.list_collections(filter={"name": collection_name})

    def delete_item(self, key: str, collection: Collection) -> bool:
        try:
            delete_result: DeleteResult = collection.delete_one({"key": key})
            return delete_result.deleted_count == 1

        except:
            return False

    def load_from_db(self, collection: Collection):
        print("this is the collection we have from hard database")
        ic(collection.find())
        return collection.find()

    @staticmethod
    def drop_all_dbs():
        dbs = client.list_database_names()

        # Drop all except system DBs
        for db in dbs:
            if db not in ["admin", "local", "config"]:
                client.drop_database(db)
                print(f"Dropped: {db}")

    @staticmethod
    def drop_peer_db(Conn):
        client.drop_database(Conn)


if __name__ == "__main__":
    HardDatabase.drop_all_dbs()
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


# Get list of all databases
