import socket
import threading
import time


from python_redis.middleware.user_cmd_mw import SocketProxyMiddleware

from python_redis.network.Server import Server, Config

# import queue
from python_redis.client import client
import os
from icecream import ic


ic.configureOutput(prefix="DEBUG: ", includeContext=True)


def main() -> None:
    server = Server.new_server(config=Config())
    try:
        server_thread: threading.Thread = threading.Thread(target=server.start)
        server_thread.start()
        time.sleep(1)
        port :int = int(os.getenv("PORT", 6001))
        print( f"port=>{port} ")
        proxy = SocketProxyMiddleware(
            listen_host="0.0.0.0",
            listen_port= port,  # Telnet connects here
            target_host="127.0.0.1",
            target_port=5001,  # Your server
        )
        proxy_thread = threading.Thread(target=proxy.start, daemon=True)
        proxy_thread.start()
        

    except KeyboardInterrupt:
        print("server stopped")
        server.stop()


# python -m python_redis.main

if __name__ == "__main__":
    main()

