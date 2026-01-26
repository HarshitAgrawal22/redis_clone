from icecream import ic
import re
from python_redis.protocols.keyval_protocol import (
    Command,
    CreateNewQueue,
)
from typing import Optional
from python_redis.common import execute_command_hash_map

ic.configureOutput(prefix="DEBUG: ", includeContext=True)


class RESP_Parser:
    def parse_command(self, raw: str) -> Optional[Command]:
        """Parses the raw RESP command bytes and returns a Command object if valid."""
        # TODO DONE learn what is RESP protocol
        # Decode raw bytes to string without removing any characters
        # print(f"raw command => {raw} {type(raw)} ")

        # ? this is the code which does all the RESP task

        ic(raw)

        # Regular expressions for RESP patterns
        # TODO: Move this resp parsinng code to resp_parser.py(need to create that )
        array_pattern = r"\*([0-9]+)\r\n"
        bulk_string_pattern = r"\$([0-9]+)\r\n(.+?)\r\n"

        # Find the array count in the RESP string
        array_match = re.match(array_pattern, raw)
        if not array_match:
            raise ValueError("Invalid RESP format (Array not found)")

        expected_items = int(array_match.group(1))
        items = re.findall(bulk_string_pattern, raw)

        # Debugging output for items parsed
        # print(f"Found items: {items}")

        # Validate RESP format

        if len(items) != expected_items:
            raise ValueError(f"RESP array length mismatch command:{raw}")
        command_name: str
        # Extract command name and arguments
        command_name, *args = [item[1] for item in items]
        try:

            func = (
                resultfunc
                if (
                    resultfunc := execute_command_hash_map.get(
                        command_name.lower().strip()
                    )
                )
                != None
                else execute_command_hash_map.get("ukc")
            )
            # print(func, "is the function we have got")

            if func != None:
                return func(args)
            # If no command matches, return None or raise an error
            else:

                raise ValueError(f"Unknown command: {command_name}")

        except Exception as e:
            print(e)

    def extract_one_resp_command(self, buffer: str) -> tuple[str | None, str]:
        """
        Extracts exactly ONE complete RESP command from a buffer.

        Parameters:
            buffer: A string that may contain:
                    - an incomplete RESP command
                    - exactly one RESP command
                    - multiple RESP commands concatenated

        Returns:
            (command, remaining_buffer)
                command            → the full RESP command as a string
                remaining_buffer   → leftover data after extracting one command

            (None, buffer) if the buffer does NOT yet contain a full command
        """

        # RESP commands must start with '*' (array type)
        # If buffer does not start with '*', protocol is invalid
        if not buffer.startswith("*"):
            raise ValueError("Invalid RESP start")

        try:
            # -----------------------------------------
            # STEP 1: Read the RESP array length
            # Example:
            #   *2\r\n
            #    ↑
            #    number of elements (argc = 2)
            # -----------------------------------------

            # Find the end of the first line (*<count>\r\n)
            line_end = buffer.find("\r\n")

            # If we haven't received "\r\n" yet,
            # the command is incomplete → wait for more data
            if line_end == -1:
                return None, buffer

            # Extract number after '*'
            # buffer[1:line_end] → "2"
            argc = int(buffer[1:line_end])

            # Move index to the first bulk string
            # Skip "*<argc>\r\n"
            idx = line_end + 2

            # -----------------------------------------
            # STEP 2: Parse each bulk string
            # -----------------------------------------
            for _ in range(argc):

                # Each bulk string must start with '$'
                if buffer[idx] != "$":
                    raise ValueError("Invalid bulk string")

                # Find end of "$<length>\r\n"
                len_end = buffer.find("\r\n", idx)

                # If length line is incomplete → wait
                if len_end == -1:
                    return None, buffer

                # Extract the bulk string length
                # Example: $4\r\n → strlen = 4
                strlen = int(buffer[idx + 1 : len_end])

                # Move index to the actual data
                idx = len_end + 2

                # Check if the buffer already contains:
                # <data> + "\r\n"
                if len(buffer) < idx + strlen + 2:
                    # Not enough data yet → wait
                    return None, buffer

                # Skip over:
                #   <data> + "\r\n"
                idx += strlen + 2

            # -----------------------------------------
            # STEP 3: Full RESP command extracted
            # -----------------------------------------

            # buffer[:idx]     → one complete RESP command
            # buffer[idx:]     → remaining data (next commands)
            return buffer[:idx], buffer[idx:]

        except Exception:
            # Any parsing error:
            # treat buffer as incomplete / invalid
            return None, buffer
