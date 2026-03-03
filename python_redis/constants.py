import os

ServerPort= ":5001"
SyncTime: int = 600
# MongoDBStr :str = "mongodb://127.0.0.1:27017/"
# MongoDBStr :str ="mongodb://mongodb:27017"
MongoDBStr:str=os.getenv("MONGO_URL")
class CommandFormat:
    error :str = "e"
    simple_string :str = "s"
    bulk_string :str = "b"
    array :str = "a"
    integer :str = "i"
