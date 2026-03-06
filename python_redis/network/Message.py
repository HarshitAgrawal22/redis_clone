from __future__ import annotations
from typing import TYPE_CHECKING
from python_redis.protocols.command import Command

if TYPE_CHECKING:
    from python_redis.network.peer import Peer


class Message:
    def __init__(self, cmd: bytearray, conn_peer: Peer):
        # this is the peer from/to this message is sent/received
        self.conn_peer: Peer = conn_peer
        self.cmd: Command = cmd

    def __str__(self):
        return f"conn_peer:{self.conn_peer}     cmd:{self.cmd}"
