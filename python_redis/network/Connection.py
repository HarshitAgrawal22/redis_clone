import socket
from icecream import ic
from python_redis.common import message_format
ic.configureOutput(prefix="DEBUG: ", includeContext=True)

# implement this function every where
class SocketConnection:
    def __init__(self,conn_from_peer:socket.socket):
        self.conn_of_peer= conn_from_peer
        # TODO : integrate it to code 
    def send(self,msg:str, type_of_message:str):
        try:
            func = message_format.get(type_of_message)
            if func!= None:
                return  self.conn_of_peer.send(func(msg))
            else:
                return "Message not sent"
        except socket.error as e :
            ic(f"Send error: {e} " )
            return None
    def close(self):
        pass