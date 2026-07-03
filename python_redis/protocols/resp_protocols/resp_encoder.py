class RESP_Encoder:
    def resp_simple_string(msg: str) -> bytes:# type: ignore
        return f"+{msg}\r\n".encode()

    def resp_error(msg: str) -> bytes:# type: ignore
        return f"-{msg}\r\n".encode()

    def resp_integer(num: int) -> bytes:# type: ignore
    
        return f":{num}\r\n".encode()

    def resp_bulk_string(val: str | None) -> bytes:# type: ignore
        if val is None:
            return b"$-1\r\n"
        return f"${len(val)}\r\n{val}\r\n".encode()

    def resp_array(items: list[str]) -> bytes:# type: ignore
        out = f"*{len(items)}\r\n"
        for item in items:
            out += f"${len(item)}\r\n{item}\r\n"
        return out.encode()

# | Prefix | Type          | Example                              |
# | ------ | ------------- | ------------------------------------ |
# | `+`   s | Simple String | `+OK\r\n`                            |
# | `-`   e | Error         | `-ERR wrong number of arguments\r\n` |
# | `:`   i | Integer       | `:10\r\n`                            |
# | `$`   b | Bulk String   | `$5\r\nvalue\r\n`                    |
# | `*`   a | Array         | `*2\r\n$3\r\none\r\n$3\r\ntwo\r\n`   |
