from typing import Any, Tuple


class RESP_Decoder:
    def decode_resp(self, data: str, index: int = 0) -> Tuple[Any, int]:
        """
        Decodes a RESP value starting at data[index].
        Returns (decoded_value, new_index).
        """

        prefix = data[index]

        # SIMPLE STRING
        if prefix == "+":
            end = data.index("\r\n", index)
            return data[index + 1 : end], end + 2

        # ERROR
        if prefix == "-":
            end = data.index("\r\n", index)
            raise Exception(data[index + 1 : end])

        # INTEGER
        if prefix == ":":
            end = data.index("\r\n", index)
            return int(data[index + 1 : end]), end + 2

        # BULK STRING
        if prefix == "$":
            end = data.index("\r\n", index)
            length = int(data[index + 1 : end])
            if length == -1:
                return None, end + 2
            start = end + 2
            return data[start : start + length], start + length + 2

        # ARRAY
        if prefix == "*":
            end = data.index("\r\n", index)
            count = int(data[index + 1 : end])
            items = []
            pos = end + 2
            for _ in range(count):
                value, pos = self.decode_resp(data, pos)
                items.append(value)
            return items, pos

        raise ValueError("Invalid RESP format")


# def parse_resp(data: bytes | str):
#     if isinstance(data, bytes):
#         data = data.decode("utf-8")
#     value, _ = decode_resp(data, 0)
#     return value
