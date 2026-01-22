import socket
import threading
import time
from typing import Dict

# TODO: write middleware python application which will convert the normal logical commands to the RESP which this redis needs and then also return the result in Human readable form which will be generated from RESP result

# TODO: add module for server's config

from python_redis.Middleware.user_cmd_mw import SocketProxyMiddleware
from python_redis.common import execute_task_hash_map, Message
from python_redis.network import peer
from queue import Queue, Empty as EmptyQueue
from python_redis.network.Server import Server, Config

# import queue
from python_redis.client import client
import python_redis.models.keyval as keyval

from icecream import ic

default_listen_address: str = ":5001"
ic.configureOutput(prefix="DEBUG: ", includeContext=True)


def main() ->                                       None:
    server = Server.new_server(config=Config())
    try:
        server_thread:threading.Thread = threading.Thread(target=server.start)
        server_thread.start()
        time.sleep(1)
        proxy = SocketProxyMiddleware(
            listen_host="127.0.0.1",
            listen_port=6001,  # Telnet connects here
            target_host="127.0.0.1",
            target_port=5001,  # Your server
        )
        proxy.start()
        
        # client.Client("127.0.0.1:5001").test_tree()
        # cl = client.Client("127.0.0.1:5001")
        # thr = threading.Thread(target=cl.set, args=("name", "Harshit"))
        # # cl.set("name", "HArshit")
        # thr.start()

        # threading.Thread(target=cl.get, args=("name",)).start()
        # thread.start()
        # cl.get("name")

        # ic(clint.get("name"))
        # (clint.insert_vertex_to_graph())
        # clint.add_edges_to_graph()
        # ic(clint.bfs())
        # clint.dij_dis()
        # clint.show_graph()
        # clint.remove_edge()
        # clint.show_graph()
        # clint.dij_shortest_path()
        # ic(clint.show_graph())
        # threading.Event().wait(1)

        # ic(server.start())
        # Using IceCream to print the return value of start()
        # time.sleep(1)

        # for i in range(10):
        #     client_server = client.Client("127.0.0.1:5001")
        #     if err := client_server.set(key=f"pakoda_{i}", value=f"aloo_{i}"):
        #         print(f"error= > {err}")
        #     try:
        #         value = client_server.get(key=f"pakoda_{i}")

        #         print(f"received value => { value}")
        #     except Exception as e:
        #         print(e)
        # time.sleep(1)
        # print(server.kv.data)
    except KeyboardInterrupt:
        print("server stopped")
        server.stop()


# python -m python_redis.main

if __name__ == "__main__":
    main()


# 🔧 1. Data Consistency
# Problem: There may be data changes between sync intervals, leading to inconsistent or outdated snapshots in MongoDB.

# Impact: A crash before a scheduled sync causes data loss.

# Mitigation: Consider implementing a write-ahead log (WAL) or event queue to replay missed changes.

# 🔃 2. Performance Overhead
# Problem: Serializing and writing large data volumes to disk every 5 minutes may cause CPU or I/O bottlenecks.

# Impact: Latency spikes or reduced responsiveness of your Redis clone.

# Mitigation: Perform writes in a background thread/process and compress or diff the data before saving.

# 📂 3. Data Modeling in MongoDB
# Problem: Redis uses varied data structures (sets, lists, graphs, trees, etc.) that may not directly map to MongoDB documents.

# Impact: Incorrect schema choices can lead to inefficient queries and storage.

# Mitigation: Design schema per data type:

# Store lists as arrays,

# Sets as arrays with uniqueness enforced,

# Graphs using reference documents,

# Trees via nested documents or adjacency lists.

# 🧵 4. Concurrency Issues
# Problem: Reads/writes may happen during a sync operation.

# Impact: May result in race conditions or corrupted snapshots.

# Mitigation: Use locking mechanisms or snapshot copies to serialize state safely.

# 🕒 5. Clock/Sync Timing
# Problem: Scheduling syncs precisely every 5 minutes can be tricky across threads or async handlers.

# Impact: Delays or overlapping writes.

# Mitigation: Use a scheduler like APScheduler, threading.Timer, or asyncio.

# 📈 6. Storage Growth and Cleanup
# Problem: Without pruning, MongoDB may grow rapidly with old data or snapshots.

# Impact: Increased disk usage and degraded performance.

# Mitigation: Use TTL indexes or regularly purge obsolete data.

# 🔁 7. Recovery Logic
# Problem: On restart, recovering from MongoDB may involve rebuilding complex structures (e.g., trees, graphs).

# Impact: Startup time becomes slow or error-prone.

# Mitigation: Store metadata or version markers for each data structure to aid reconstruction.

# ✅ Summary
# Challenge	Risk	Recommendation
# Data Loss	Mid-sync crash	Use WAL/event queue
# CPU/I/O Overhead	Performance dips	Background writing & compression
# Schema Mismatch	Inefficient data use	Tailored schema for each structure
# Concurrency	Data race/corruption	Locking or consistent snapshot strategy
# Timing Drift	Missed or overlapping writes	Reliable async scheduler
# Storage Bloat	Disk overflow	TTL, cleanup jobs
# Complex Recovery	Error-prone restarts	Store metadata with structure dumps
