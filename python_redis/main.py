import socket
import threading
from typing import Dict
import protocol
from protocol import SetCommand, GetCommand, Command
import peer
import time
from icecream import ic
from queue import Queue
from client import client
import keyval

default_listen_address: str = ":5001"
ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class Config:
    def __init__(self, listen_address: str = default_listen_address):
        # It holds data like "ListenAddress," specifying where the server listens for connections
        self.listen_address: str = listen_address


class Message:
    def __init__(self, cmd: bytearray, conn_peer):
        self.conn_peer: peer.Peer = conn_peer
        self.cmd: Command = cmd

    def __str__(self):
        return f"conn_peer:{self.conn_peer}     cmd:{self.cmd}"


class Server:
    def __init__(self, config: Config):
        # Server holds settings, a list of peers, a listener, and a channel for new peers.
        self.config: Config = config
        self.peers: Dict[peer.Peer, bool] = (
            {}
        )  # Dict to track connected peers with Peer as keys
        self.listener: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # Network listener
        self.add_peer_ch: list[peer.Peer] = []  # Channel to add peers to the server
        self.del_peer_ch: list[peer.Peer] = []
        # Channel to delete connection of a peer from the server
        self.quit_event = threading.Event()
        self.msg_queue = Queue()  # Queue to manage message for broadcasting
        self.kv: keyval.KV = keyval.KV.NewKV()

    @staticmethod
    def new_server(config: Config) -> "Server":
        # Initializes the server instance with config settings
        if len(config.listen_address) == 0:
            config.listen_address = default_listen_address
        return Server(config)

    def start(self) -> None:
        # Starts the server by binding to the configured address and entering the accept loop
        try:
            self.listener.bind(
                (
                    self.config.listen_address.split(":")[0],
                    int(self.config.listen_address.split(":")[1]),
                )
            )
            self.listener.listen()
            print(
                f"Server started, listening on {self.config.listen_address}"
            )  # Added print statement

            threading.Thread(target=self.loop, daemon=True).start()
            self.accept_loop()
        except Exception as e:
            print(f"Error starting server: {e}")

    def handle_message(self, msg: Message):
        if isinstance(msg.cmd, protocol.GetMultipleAttributeCommand):
            try:
                ic(msg.cmd.key)
                ic(msg.cmd.attrs)
                result = self.kv.get_attributes(msg.cmd.key, msg.cmd.attrs)
                msg.conn_peer.send(f"{result}".encode("utf-8"))
            except Exception as e:
                print(f"got error in SET_MULTIPLE_ATTRIBUTES {e}")
        if isinstance(msg.cmd, protocol.SetMultipleAttributeCommand):
            try:
                ic(msg.cmd.key)
                ic(msg.cmd.attrs)
                self.kv.set_attributes(msg.cmd.key, msg.cmd.attrs)
                msg.conn_peer.send("OK".encode("utf-8"))
            except Exception as e:
                print(f"got error in SET_MULTIPLE_ATTRIBUTES {e}")
        if isinstance(msg.cmd, protocol.SetMultipleKeyValCommand):
            try:
                ic(msg.cmd.args)
                self.kv.set_multiple_pairs(msg.cmd.args)

                msg.conn_peer.send("OK".encode("utf-8"))
            except Exception as e:

                print(f"got error in SET_MULTIPLE_KEY_VAL_COMMAND{e}")

        if isinstance(msg.cmd, protocol.GetMultipleKeyValCommand):
            try:
                ic(msg.cmd.keys)
                result: str = self.kv.get_multiple_values(msg.cmd.keys)
                msg.conn_peer.send(f"{result}".encode("utf-8"))
            except Exception as e:
                print(f"got error in CLIENT command: {e}")

        if isinstance(msg.cmd, protocol.IncrementCommand):
            try:
                self.kv.increment(msg.cmd.key)
                msg.conn_peer.send("OK".encode("utf-8"))
            except Exception as e:
                print(f"got error in CLIENT command: {e}")

        if isinstance(msg.cmd, protocol.TotalCommand):
            try:
                length: int = self.kv.total()

                msg.conn_peer.send(f"{length}".encode("utf-8"))
            except Exception as e:
                print(f"got error in CLIENT command: {e}")

        if isinstance(msg.cmd, protocol.DeleteCommand):
            try:
                self.kv.delete_pair(msg.cmd.key)
                msg.conn_peer.send("Ok".encode("utf-8"))
            except Exception as e:
                print(f"got error in CLIENT command: {e}")

        if isinstance(msg.cmd, protocol.ClientCommand):
            try:
                msg.conn_peer.send("OK".encode("utf-8"))
            except Exception as e:
                print(f"got error in CLIENT command: {e}")

        if isinstance(msg.cmd, protocol.CheckCommand):
            try:

                result: list[bool] = self.kv.check(msg.cmd.keys)
                data = "OK "
                for i in result:
                    data += f"{i} "
                msg.conn_peer.send(data.encode("utf-8"))

            except Exception as e:
                print(f"got error while CHECK command: {e}")

        if isinstance(msg.cmd, protocol.HelloCommand):
            spec = dict({"server": "redis"})
            try:
                msg.conn_peer.send(f"{spec}".encode("utf-8"))
            except:
                print("got error while sending specs")

        if isinstance(msg.cmd, protocol.QuitCommand):
            self.stop()
        if isinstance(msg.cmd, protocol.SetCommand):
            print(
                f"Somebody wants to set a key into the hash table \nkey=>{msg.cmd.key}\nvalue =>{msg.cmd.value}"
            )
            # msg.conn_peer.send(
            #     f"key=>{msg.cmd.key}\nvalue =>{msg.cmd.value}".encode("utf-8")
            # )
            try:
                msg.conn_peer.send("OK".encode("utf-8"))

                return self.kv.set(msg.cmd.key, msg.cmd.value)
            except Exception as e:
                print(f"got exception while sending SET message  {e}")
        if isinstance(msg.cmd, protocol.GetCommand):
            try:
                (value, isok) = self.kv.get(msg.cmd.key)

                # if not ok:
                #     raise ValueError("response not ok ")
                try:
                    msg.conn_peer.send(value)
                except Exception as e:
                    return e
            except ValueError as e:
                return e
        print(type(msg.cmd))
        return None

    def loop(self) -> None:
        # This loop waits for a peer in add_peer_ch and adds to the peers dict
        while not self.quit_event.is_set():

            if not self.msg_queue.empty():
                # print("analyzing command")
                msg: Message = self.msg_queue.get()

                # if msg.cmd.decode("utf-8") != "quit\r\n":
                # print(raw_msg.decode("utf-8"))
                err = self.handle_message(msg)
                if err:
                    print(f"Raw Message Error-> {err}")

                # else:  # if we get quit message from any server then the server is stopped
                # self.stop()
                # this is for development phase only

            if self.add_peer_ch:
                peer = self.add_peer_ch.pop(0)
                self.peers[peer] = True
                print(
                    f"Added new peer: {peer.Conn.getpeername()}"
                )  # Added print statement
                # if self.del_peer_ch:
                # this_peer = self.del_peer_ch.pop(0)
                # ic(self.peers)
                # del self.peers[this_peer]
                # print(f"Deleted peer: {this_peer.Conn.getpeername()}")
            else:
                threading.Event().wait(0.5)
                # slight delay tp prevent busy waiting
                # print("No new peer is received")

    def accept_loop(self) -> None:
        # Accepts incoming connections in a loop, handling each connection concurrently
        while not self.quit_event.is_set():
            try:
                conn, addr = self.listener.accept()
                print(f"Accepted a new connection from {addr}")  # Added print statement
                thread = threading.Thread(
                    target=self.handle_conn, args=(conn,), daemon=True
                )
                thread.start()
            except Exception as e:
                print(f"Accept error: {e}")

    def handle_conn(self, conn: socket.socket) -> None:
        # Handles each new connection by creating a Peer instance
        this_peer: peer.Peer = peer.Peer.newPeer(
            conn, self.msg_queue, self.del_peer_ch
        )  # here we are provinng the conn and msg_queue of server's to the Peer
        print(f"Handling connection for peer: {this_peer}")
        # this_peer.test_protocol()
        self.add_peer_ch.append(this_peer)
        # added new peer to the add_peer_ch of server
        ic(conn.getpeername())
        # starting the peer's readloop on a seperate thread to isolate each peer;s connection from every other peer
        thread = threading.Thread(target=this_peer.read_loop)
        thread.start()

    def stop(self) -> None:
        # stops the server gracefully
        self.quit_event.set()
        self.listener.close()
        print("Server stopped")


def main() -> None:
    server = Server.new_server(config=Config())
    try:
        server_thread = threading.Thread(target=server.start)
        server_thread.start()
        # ic(server.start())
        # Using IceCream to print the return value of start()
        # time.sleep(1)

        # for i in range(10):
        #     client_server = client.Client("127.0.0.1:5001")
        #     if err := client_server.set(key=f"pakoda_{i}", value=f"aloo_{i}"):
        #         print(f"error= > {err}")
        #     try:
        #         threading.Event.wait(1)
        #         value = client_server.get(key=f"pakoda_{i}")

        #         print(f"received value => { value}")
        #     except Exception as e:
        #         print(e)
        # time.sleep(1)
        # print(server.kv.data)
    except KeyboardInterrupt:
        print("server stopped")
        server.stop()


if __name__ == "__main__":
    main()
