import socket
import socketserver


class Config:
    def __init__(self, ListenAddress):

        self.ListenAddress: str = ListenAddress


class Server:
    def __init__(self, config, listener):
        self.config: Config = config
        self.listener = listener


def main():
    pass


if __name__ == "__main__":
    main()
