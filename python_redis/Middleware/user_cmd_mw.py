import socket
import threading
from icecream import ic
from python_redis.protocols.resp_protocols.resp_decoder import RESP_Decoder
BUFFER_SIZE = 4096

# Maximum number of bytes to read at once from a socket

ic.configureOutput(prefix="DEBUG: ", includeContext=True)

class SocketProxyMiddleware:
    """
    This class acts as a TCP proxy (middleware).

    Flow:
        Telnet Client
              |
              v
        [ Middleware Proxy ]
              |
              v
        Redis-like Server

    It sits in the middle, forwards data both ways,
    and logs commands sent by the client.
    """

    def __init__(
        self, listen_host: str, listen_port: int, target_host: str, target_port: int
    ):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.target_host = target_host
        self.target_port = target_port

    def start(self) -> None:
        """
        Starts the proxy server.
        This function:
        1. Creates a TCP socket
        2. Binds it to listen_host:listen_port
        3. Accepts incoming telnet connections
        4. Spawns a thread per client
        """
        proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_server.bind((self.listen_host, self.listen_port))
        proxy_server.listen()

        print(
            f"[Middleware] Listening on {self.listen_host}:{self.listen_port} "
            f"→ forwarding to {self.target_host}:{self.target_port}"
        )

        while True:
            client_sock, addr = proxy_server.accept()
            print(f"[Middleware] Telnet connected from {addr}")

            threading.Thread(
                target=self.handle_client,
                args=(client_sock,),
                daemon=True,
            ).start()

    def handle_client(self, client_sock: socket.socket) -> None:
        """
        Handles a single telnet client.

        Steps:
        1. Connect to the real server
        2. Start two forwarding threads:
           - client → server
           - server → client
        """
        try:
            target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_sock.connect((self.target_host, self.target_port))
        except Exception as e:
            print(f"[Middleware] Failed to connect to target: {e}")
            client_sock.close()
            return

        threading.Thread(
            target=self.forward,
            args=(client_sock, target_sock, "CLIENT → SERVER"),
            daemon=True,
        ).start()

        threading.Thread(
            target=self.forward,
            args=(target_sock, client_sock, "SERVER → CLIENT"),
            daemon=True,
        ).start()

    def forward(
        self,
        source: socket.socket,
        destination: socket.socket,
        direction: str,
    ) -> None:
        """
        Forwards data from one socket to another.

        source       → socket we READ from
        destination  → socket we WRITE to
        direction    → string used for logging
        """
        try:
            while True:
                data = source.recv(BUFFER_SIZE)
                if not data:
                    break

                # 🔥 LOGGING POINT
                if direction == "CLIENT → SERVER":
                    try:
                        text = data.decode("utf-8", errors="replace")
                        print(f"[Middleware] {direction}: {text.strip()}")
                        arr_len = len(holder_arr := text.split())
                        raw: str = f"*{arr_len}\r\n"
                        for i in holder_arr:
                            temp_str = i
                            raw += f"${len(i)}\r\n{temp_str}"
                            raw += "\r\n"
                        raw = raw.encode("utf-8")
                        ic(raw)
                        data = raw
                    except Exception:
                        print(f"[Middleware] {direction}: <binary data>")
                else:
                    text = data.decode("utf-8", errors="replace")
                    data = RESP_Decoder.decode_resp(text)
                    data.encode("utf-8")
                destination.sendall(data)

        except Exception as e:
            print(f"[Middleware] {direction} error: {e}")
        finally:
            source.close()
            destination.close()
