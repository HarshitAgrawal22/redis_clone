from pymongo import MongoClient, DESCENDING
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, DeleteResult
from icecream import ic
from pymongo.database import Database
from pymongo.cursor import Cursor


client = MongoClient("mongodb://127.0.0.1:27017/")

from icecream import ic

default_listen_address: str = ":5001"
ic.configureOutput(prefix="DEBUG: ", includeContext=True)
# TODO implement pub/sub model to this project, the instructions are written at the bottom of this file


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

    def insert_and_update_item(self, item: str, collection: Collection):
        try:
            print(
                f"Inserting data to mongodb=> Key:key, value: {item}, collection: {collection}"
            )
            update_result = collection.update_one(
                {"value": item}, {"$set": {"value": item}}, upsert=True
            )
            return True
        except Exception as e:
            ic(e)
            return False

    def insert_and_update_key_val(self, key: str, value: str, collection: Collection):
        try:
            # print(
            # f"Inserting data to mongodb=> Key:{key}, value: {value}, collection: {collection} "
            # )
            update_result = collection.update_one(
                {"key": key}, {"$set": {"key": key, "value": value}}, upsert=True
            )
            return update_result.modified_count > 0
        except Exception as e:
            ic(e)
            return False

    def insert_and_update_ordered_items(
        self, value: str, index: int, collection: Collection
    ):
        update_result = collection.update_one(
            {"index": index}, {"$set": {"index": index, "value": value}}, upsert=True
        )
        return update_result.modified_count > 0

    def check_collection_exist(self, collection_name: str) -> bool:
        # return self.db.list_collections(limit=1).alive
        return self.db.list_collections(filter={"name": collection_name})

    def delete_key(self, key: str, collection: Collection) -> bool:
        try:
            delete_result: DeleteResult = collection.delete_one({"key": key})
            return delete_result.deleted_count == 1

        except:
            return False

    def delete_item(self, value: str, collection: Collection) -> bool:
        try:
            delete_result: DeleteResult = collection.delete_one({"value": value})
            return delete_result.deleted_count == 1

        except:
            return False

    def delete_dequeue_item(self, value: str, collection: Collection) -> bool:
        try:
            # delete_result: DeleteResult = collection.delete_one({"value": value})
            delete_result: DeleteResult = collection.find_one_and_delete(
                {}, sort=[("index", 1)]
            )
            return delete_result.deleted_count == 1

        except:
            return False

    def delete_stack_item(self, value: str, collection: Collection) -> bool:
        try:
            # delete_result: DeleteResult = collection.delete_one({"value": value})
            delete_result: DeleteResult = collection.find_one_and_delete(
                {}, sort=[("index", DESCENDING)]
            )
            return delete_result.deleted_count == 1

        except:
            return False

    def load_from_db(self, collection: Collection) -> Cursor:
        print("this is the collection we have from hard database")
        docs = list(collection.find())
        ic(docs)

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


# Ah, I see what you mean now 👍 You’re asking:

# 👉 Inside Redis, is Pub/Sub only for message brokering?

# The answer:

# Yes — in Redis, Pub/Sub is specifically designed for message passing (broker-like behavior).

# Redis Pub/Sub does not touch or affect the key-value database itself.

# It does not cache data.

# It does not persist data.

# It does not update keys/values in Redis.

# It is only a real-time messaging mechanism.

# Key points about Redis Pub/Sub:

# Works like a lightweight message broker.

# Messages are sent directly from publishers to subscribers via channels.

# Redis does not store or replay messages — if no subscriber is listening, the message is lost.

# It’s good for notifications, chat, signaling, real-time updates.

# If you want something that keeps messages for later (like a queue), Redis provides Redis Streams or you can use lists as queues.

# ✅ So yes, Redis Pub/Sub is only for the message broker role — it does not integrate with Redis’ caching or persistence directly.

# Do you want me to also explain how Redis Streams extend Pub/Sub to add durability and replay?


# Good question 👍 Let’s carefully separate the concepts:

# Redis Pub/Sub (built-in)

# Independent of caching: Pub/Sub channels are completely separate from Redis keys.

# You cannot directly say “notify me when key X changes” with plain Pub/Sub.

# Messages in Pub/Sub are transient — once delivered (or if no subscriber exists), they are gone.

# But can we implement Pub/Sub around caching?

# Yes ✅ — but not with raw Pub/Sub alone. You’d combine Redis’ caching features with Pub/Sub or Streams:

# Manual Publish on Cache Updates

# When your app updates a cache key (e.g., SET user:1 "Harsh"), it also PUBLISH "user_updates" "user:1".

# Subscribers listen on "user_updates" and know which cached items changed.

# This way you "tie" caching to Pub/Sub yourself.

# Keyspace Notifications (special Redis feature)

# Redis has a feature called Keyspace Notifications (notify-keyspace-events).

# It lets you subscribe to events like SET, DEL, EXPIRE on keys.

# Example: SUBSCRIBE "__keyspace@0__:user:1" → gets a notification whenever key user:1 changes.

# This is Pub/Sub for cache events, built directly into Redis.

# Redis Streams for Reliable Pub/Sub with Cache

# If you need to store events (not lose them), use Redis Streams instead of basic Pub/Sub.

# Example: every time cache is updated, also XADD cache_updates ....

# Consumers can replay events, unlike ephemeral Pub/Sub.

# Summary

# Default Pub/Sub = only message broker (no caching link).

# But you can implement Pub/Sub with caching by:

# (a) publishing manually on cache updates,

# (b) using Keyspace Notifications to auto-publish events,

# (c) using Streams for durability.

# 👉 So yes, you can integrate Pub/Sub into caching logic, but you must explicitly wire it up (via notifications or publishing).

# Would you like me to show you a small Python example where a cache SET triggers Pub/Sub so subscribers get notified?


# In Redis, Pub/Sub is a general feature, but it shows up in different contexts. Let’s break them down:

# 1. Classic Pub/Sub (Message Broker Style)

# You explicitly PUBLISH to a channel, and clients SUBSCRIBE or PSUBSCRIBE to listen.

# Example use cases:

# Chat applications

# Notifications between services

# Event-driven systems

# ⚡ Key point: Messages are fire-and-forget (if no one is listening, the message is gone).

# 2. Keyspace Notifications (Pub/Sub + Caching)

# When enabled (CONFIG SET notify-keyspace-events ...), Redis publishes events when keys are changed (set, del, expire, etc.).

# Subscribers listen on special channels (__keyspace@db__:key or __keyevent@db__:event).

# Example use cases:

# Cache invalidation across services

# Real-time monitoring of keys

# Triggers for background jobs when data changes

# 3. Streams (Redis ≥ 5.0)

# Technically not the same as classic Pub/Sub, but often compared.

# Streams provide a durable Pub/Sub model with persistence and consumer groups.

# Example use cases:

# Reliable message queues

# Event sourcing

# Distributed data pipelines

# ⚡ Difference: Unlike classic Pub/Sub, messages in Streams are stored until acknowledged.

# 4. Modules and Internal Features

# Some Redis modules or patterns internally rely on Pub/Sub:

# RedisGears or custom triggers can use Pub/Sub to fire events.

# Monitoring tools use Pub/Sub channels to watch server activity.

# ✅ So, Pub/Sub in Redis is used in three main places:

# Direct messaging (classic PUBLISH / SUBSCRIBE)

# Keyspace notifications (events when keys change)

# Streams (durable, advanced Pub/Sub with persistence)

# Would you like me to make a diagram showing how these three Pub/Sub usages differ? That might make the picture crystal clear.


# You’re raising an important point here 👍

# Let me carefully break it down:

# ✅ Redis as Cache

# When people say “Redis is used as a cache”, they usually mean:

# Store frequently accessed data in RAM for super-fast reads/writes.

# Examples:

# Cache results of SQL queries

# Cache API responses

# Store session tokens

# ⚡ By default, Redis stores data in memory (RAM), not on disk.
# That’s why it is so fast but also volatile (data can be lost if Redis restarts).

# ✅ Redis as Durable Store

# Redis is not just a cache. It can also be configured as a durable database:

# RDB snapshots: Periodically dumps the dataset to disk.

# AOF (Append Only File): Logs every write operation for replay after restart.

# Hybrid mode: Use both RDB + AOF for better balance between performance and durability.

# ⚡ With these persistence options, Redis can behave more like a NoSQL database than just a cache.

# ✅ Redis as Message Broker

# On top of caching and durability, Redis implements:

# Pub/Sub channels (fast, ephemeral messaging)

# Streams (persistent, durable messaging system with consumer groups)

# So answering your question:

# “Does Redis used for caching include all features like durable database?”

# ❌ No — caching is only one of Redis’s roles.
# ✅ Redis can also be a durable database if you enable persistence.
# ✅ Redis can also be a message broker (Pub/Sub, Streams).

# 👉 In short:

# If you use Redis only as a cache → it’s just fast, volatile storage in RAM.

# If you enable persistence → it becomes a durable DB.

# If you use Pub/Sub → it’s a message broker.

# Would you like me to map out Redis’s “modes of use” (cache, DB, broker) side by side so you can see clearly how people use it differently?
