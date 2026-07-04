import socket
from icecream import ic
from python_redis.common import message_format
ic.configureOutput(prefix="DEBUG: ", includeContext=True)

# implement this function every where
class SocketConnection:
    def __init__(self,conn_from_peer:socket.socket):
        self.conn_of_peer= conn_from_peer
       
    def send(self,msg:str, type_of_message:str):
        try:
            func = message_format.get(type_of_message)
            if func!= None:
                
                return  self.conn_of_peer.sendall(func(msg))
            else:
                return "Message not sent"
        except socket.error as e :
            ic(f"Send error: {e} ")
            return None
    def close(self):
            

        try:
            self.send("Bye! thanks for using redis", "b")
            # Step 1: Shutdown both send & receive
            self.conn_of_peer.shutdown(socket.SHUT_RDWR)
        except OSError as oe:
            # already closed or reset
            print(f"Encountered OS  error=> {oe}")
            pass
        finally:
            # Step 2: Close the socket

            self.conn_of_peer.close()
            # self.del_peer_chan.put(self)

            # Step 3: Cleanup peer DB
            #  sudo service mongod start
            # HardDatabase.drop_peer_db(self.DB_str)

            # print(f"Closed connection for {self}")
