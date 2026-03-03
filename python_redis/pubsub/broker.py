# TODO: add code for pub sub module here
import threading
from typing import Dict, Set

class PubSubBroker:
    def __init__(self):
        self.channels :Dict[str, Set]= dict()
        self.lock= threading.RLock()
        
    def subscribe(self, channel:str, peer)->None:
        with self.lock:
            if channel not in self.channels:
                self.channels[channel]= set()
                self.channels[channel].add(peer)
                
    def unsubscribe(self, channel:str, peer):
        with self.lock:
            if channel in self.channels:
                self.channels[channel].discard(peer)
                if not self.channels[channel]:
                    del self.channels[channel]
                
    def publish(self, channel :str , message :str)-> int:
        with self.lock:
            subscribers= list(self.channels.get(channel, []))
        for peer in subscribers:
            try:
                peer.send( f"*3\r\n"
                    f"$7\r\nmessage\r\n"
                    f"${len(channel)}\r\n{channel}\r\n"
                    f"${len(message)}\r\n{message}\r\n"
                    .encode())
            except Exception :
                pass
        return len(subscribers)
    
    def remove_peer(self, peer)-> None:
        with self.lock:
            for channel in list(self.channels.keys()):
                self.channels[channel].discard(peer)
                if not self.channels[channel]:
                    del self.channels[channel]