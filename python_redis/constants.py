import os

ServerPort= ":5001"
SyncTime: int = 6
# MongoDBStr :str = "mongodb://127.0.0.1:27017/"
MongoDBStr :str ="mongodb://mongodb:27017"
# MongoDBStr:str=os.getenv("MONGO_URL")

class CommandFormat:
    error :str = "e"
    simple_string :str = "s"
    bulk_string :str = "b"
    array :str = "a"
    integer :str = "i" 
class DbConnectionStrings:
    class Graph:
        pass 
    class List:
        pass 
    class Keyval:
        pass 
    class Queue:
        pass 
    class Set:
        pass 
    class Tree:
        pass 
    class Stack:
        pass 