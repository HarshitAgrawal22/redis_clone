from icecream import ic
from python_redis.network.Message import Message


ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class HASHMAP_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_unknown_command(msg: Message, server):
        try:
            msg.conn_peer.send(msg.cmd.response.encode("utf-8"))
        except Exception as e:
            print(f"got exception while processing unknown command:  {e}")

    @staticmethod
    def task_set_command(msg: Message, server):
        # print(
        #     f"Somebody wants to set a key into the hash table \nkey=>{msg.cmd.key}\nvalue =>{msg.cmd.value}"
        # )
        # msg.conn_peer.send(
        #     f"key=>{msg.cmd.key}\nvalue =>{msg.cmd.value}".encode("utf-8")
        # )
        try:
            msg.conn_peer.send("OK".encode("utf-8"))

            return msg.conn_peer.kv.set(msg.cmd.key, msg.cmd.value)
        except Exception as e:
            print(f"got exception while sending SET message  {e}")

    @staticmethod
    def task_get_command(msg, server):

        try:
            (value, isOK) = msg.conn_peer.kv.get(msg.cmd.key)

            # if not OK:
            #     raise ValueError("response not OK ")
            try:
                msg.conn_peer.send(f"{value}".encode("utf-8"))
            except Exception as e:
                return e
        except ValueError as e:
            return e

    @staticmethod
    def task_total_command(msg, server):

        try:
            length: int = msg.conn_peer.kv.total()

            msg.conn_peer.send(f"{length}".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_get_multiple_attrs_command(msg, server):
        try:
            ic(msg.cmd.key)
            ic(msg.cmd.attrs)
            result = msg.conn_peer.kv.get_attributes(msg.cmd.key, msg.cmd.attrs)
            msg.conn_peer.send(f"{result}".encode("utf-8"))
        except Exception as e:
            print(f"got error in SET_MULTIPLE_ATTRIBUTES {e}")

    @staticmethod
    def task_set_multiple_attrs_command(msg, server):
        try:
            ic(msg.cmd.key)
            ic(msg.cmd.attrs)
            msg.conn_peer.kv.set_attributes(msg.cmd.key, msg.cmd.attrs)
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(f"got error in SET_MULTIPLE_ATTRIBUTES {e}")

    @staticmethod
    def task_set_multi_key_val_command(msg: Message, server):
        try:
            ic(msg.cmd.args)
            msg.conn_peer.kv.set_multiple_pairs(msg.cmd.args)

            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:

            print(f"got error in SET_MULTIPLE_KEY_VAL_COMMAND{e}")

    @staticmethod
    def task_get_multi_key_val_command(msg, server):
        try:
            ic(msg.cmd.keys)
            result: str = msg.conn_peer.kv.get_multiple_values(msg.cmd.keys)
            msg.conn_peer.send(f"{result}".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_quit_command(msg: Message, server):

        server.stop()

    @staticmethod
    def task_kill_command(msg: Message, server):
        try:
            print(str(f"Closed the connection from :{msg.conn_peer}"))
            msg.conn_peer.close_connection()
            # raise OSError("breaking connection from client ")
        except Exception as e:
            print(f"Exception while breaking connection=> {e}")

    @staticmethod
    def task_increment_command(msg: Message, server):
        try:
            msg.conn_peer.kv.increment(msg.cmd.key)
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_delete_command(msg: Message, server):
        try:
            msg.conn_peer.kv.delete_pair(msg.cmd.key)
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_client_command(msg, server):

        try:
            msg.conn_peer.send("OK".encode("utf-8"))
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_check_command(msg, server):
        try:

            result: list[bool] = msg.conn_peer.kv.check(msg.cmd.keys)
            data = "OK "
            for i in result:
                data += f"{i} "
            msg.conn_peer.send(data.encode("utf-8"))

        except Exception as e:
            print(f"got error while CHECK command: {e}")

    @staticmethod
    def task_hello_command(msg, server):
        spec = dict({"server": "redis"})
        try:
            msg.conn_peer.send(f"{spec}".encode("utf-8"))
        except:
            print("got error while sending specs")
