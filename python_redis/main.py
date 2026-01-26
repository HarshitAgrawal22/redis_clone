import socket
import threading
import time
from typing import Dict

# TODO: write middleware python application which will convert the normal logical commands to the RESP which this redis needs and then also return the result in Human readable form which will be generated from RESP result

# TODO: add module for server's config

from python_redis.middleware.user_cmd_mw import SocketProxyMiddleware

from python_redis.network.Server import Server, Config

# import queue
from python_redis.client import client

from icecream import ic

default_listen_address: str = ":5001"
ic.configureOutput(prefix="DEBUG: ", includeContext=True)


def main() -> None:
    server = Server.new_server(config=Config())
    try:
        server_thread: threading.Thread = threading.Thread(target=server.start)
        server_thread.start()
        time.sleep(1)
        # proxy = SocketProxyMiddleware(
        #     listen_host="127.0.0.1",
        #     listen_port=6001,  # Telnet connects here
        #     target_host="127.0.0.1",
        #     target_port=5001,  # Your server
        # )
        # proxy.start()
        proxy = SocketProxyMiddleware(
            listen_host="0.0.0.0",
            listen_port=6001,  # Telnet connects here
            target_host="127.0.0.1",
            target_port=5001,  # Your server
        )
        proxy_thread = threading.Thread(target=proxy.start, daemon=True)
        proxy_thread.start()
        # proxy.start()
        # client.Client("127.0.0.1:6001").test_tree()
        cl = client.Client("127.0.0.1:5001")
        thr = threading.Thread(target=cl.set, args=("name", "Harshit"))
        # cl.set("name", "HArshit")
        thr.start()

        threading.Thread(target=cl.get, args=("name",)).start()
        # thread.start()
        # cl.get("name")

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

# mongoDB problem
# 🕒 5. Clock/Sync Timing
# Problem: Scheduling syncs precisely every 5 minutes can be tricky across threads or async handlers.

# Impact: Delays or overlapping writes.

# Mitigation: Use a scheduler like APScheduler, threading.Timer, or asyncio.
