import socket
import threading
from typing import Dict
import peer
from icecream import ic
from queue import Queue


class Command:
    def __init__(self):
        pass


def parse_command(msg_queue: Queue):
    return Command(), None
