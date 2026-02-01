from icecream import ic

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

def ic_ok(msg: str) -> None:
    ic(f"{GREEN}OK: {msg}{RESET}")

def ic_warn(msg: str) -> None:
    ic(f"{YELLOW}WARN: {msg}{RESET}")

def ic_error(msg: str) -> None:
    ic(f"{RED}ERROR: {msg}{RESET}")

ic.configureOutput(prefix="")
ic_ok("Server started")
ic_warn("High latency detected")
ic_error("Connection dropped")
