class RESP_Encoder:
    def resp_simple_string(msg: str) -> bytes:
        return f"+{msg}\r\n".encode()

    def resp_error(msg: str) -> bytes:
        return f"-{msg}\r\n".encode()

    def resp_integer(num: int) -> bytes:
    
        return f":{num}\r\n".encode()

    def resp_bulk_string(val: str | None) -> bytes:
        if val is None:
            return b"$-1\r\n"
        return f"${len(val)}\r\n{val}\r\n".encode()

    def resp_array(items: list[str]) -> bytes:
        out = f"*{len(items)}\r\n"
        for item in items:
            out += f"${len(item)}\r\n{item}\r\n"
        return out.encode()

