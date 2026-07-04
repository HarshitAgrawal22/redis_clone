from icecream import ic
from python_redis.network.Message import Message


ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class HASHMAP_TASKS:
    def __init__(self):
        print(self)

    @staticmethod
    def task_unknown_command(msg: Message, server):
        try:
            msg.conn_peer.socket_handler.send(msg.cmd.response,"e") # type:ignore
        except Exception as e:
            print(f"got exception while processing unknown command:  {e}")

    @staticmethod
    def task_set_command(msg: Message, server):
        try:
            msg.conn_peer.kv.set(msg.cmd.key, msg.cmd.value)# type:ignore
            msg.conn_peer.socket_handler.send("OK","s")

        except Exception as e:
            print(f"got exception while sending SET message  {e}")

    @staticmethod
    def task_get_command(msg: Message, server):

        try:
            (value, isOK) = msg.conn_peer.kv.get(msg.cmd.key)# type:ignore

            # if not OK:
            #     raise ValueError("response not OK ")
            try:
                msg.conn_peer.socket_handler.send(f"{value}", "b")
            except Exception as e:
                return e
        except ValueError as e:
            return e

    @staticmethod
    def task_total_command(msg: Message, server):

        try:
            length: int = msg.conn_peer.kv.total()

            msg.conn_peer.socket_handler.send(f"{length}", "i")
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_get_multiple_attrs_command(msg :Message, server):
        try:
            ic(msg.cmd.key)# type:ignore
            ic(msg.cmd.attrs)# type:ignore
            result = msg.conn_peer.kv.get_attributes(msg.cmd.key, msg.cmd.attrs)# type:ignore
            final_response= result.split(" ")
            ic(final_response)
            msg.conn_peer.socket_handler.send(final_response, "a")# type:ignore
        except Exception as e:
            print(f"got error in SET_MULTIPLE_ATTRIBUTES {e}")

    @staticmethod
    def task_set_multiple_attrs_command(msg:Message, server):
        try:
            ic(msg.cmd.key)# type:ignore
            ic(msg.cmd.attrs)# type:ignore
            msg.conn_peer.kv.set_attributes(msg.cmd.key, msg.cmd.attrs)# type:ignore
            msg.conn_peer.socket_handler.send("OK", "s")
        except Exception as e:
            print(f"got error in SET_MULTIPLE_ATTRIBUTES {e}")

    @staticmethod
    def task_set_multi_key_val_command(msg: Message, server):
        try:
            ic(msg.cmd.args)# type:ignore
            msg.conn_peer.kv.set_multiple_pairs(msg.cmd.args)# type:ignore

            msg.conn_peer.socket_handler.send("OK","s")
        except Exception as e:

            print(f"got error in SET_MULTIPLE_KEY_VAL_COMMAND{e}")

    @staticmethod
    def task_get_multi_key_val_command(msg, server):
        try:
            ic(msg.cmd.keys)
            result: str = msg.conn_peer.kv.get_multiple_values(msg.cmd.keys)
            msg.conn_peer.socket_handler.send(result.split(" "), "a")
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
            msg.conn_peer.kv.increment(msg.cmd.key)# type:ignore
            msg.conn_peer.socket_handler.send("OK", "s")
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_delete_command(msg: Message, server):
        try:
            msg.conn_peer.kv.delete_pair(msg.cmd.key)# type:ignore
            msg.conn_peer.socket_handler.send("OK","s")
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_client_command(msg: Message, server):

        try:
            msg.conn_peer.socket_handler.send("OK", "s")
        except Exception as e:
            print(f"got error in CLIENT command: {e}")

    @staticmethod
    def task_check_command(msg: Message, server):
        try:

            result: list[bool] = msg.conn_peer.kv.check(msg.cmd.keys)# type:ignore
            data = "OK "
            for i in result:
                data += f"{i} "
            msg.conn_peer.socket_handler.send(data.split(), "a")# type:ignore

        except Exception as e:
            print(f"got error while CHECK command: {e}")

    @staticmethod
    def task_hello_command(msg: Message, server):
        spec = dict({"server": "redis"})
        try:
            msg.conn_peer.socket_handler.send(list( spec.items()), "a")# type:ignore
        except:
            print("got error while sending specs")
