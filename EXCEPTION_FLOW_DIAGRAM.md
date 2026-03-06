# Global Exception Handler - Flow Diagram

## Exception Handling Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT REQUEST                           │
│                              ↓                                   │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Peer.read_loop()                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  try:                                                        │ │
│  │     1. Receive data from socket                             │ │
│  │     2. Decode data                                          │ │
│  │     3. Parse RESP command ──┐                               │ │
│  │                              │ Exception?                    │ │
│  │  except Exception as e: ←───┘                               │ │
│  │     GlobalExceptionHandler.handle_parsing_exception(e)      │ │
│  │     Send RESP error to client                               │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               ↓
                    Add message to msg_queue
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Server.loop()                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  try:                                                        │ │
│  │     Get message from queue                                  │ │
│  │     try:                                                     │ │
│  │        handle_message(msg) ──┐                              │ │
│  │                               │ Exception?                   │ │
│  │     except Exception as e: ←─┘                              │ │
│  │        GlobalExceptionHandler.handle_message_exception(e)   │ │
│  │        Send RESP error to client                            │ │
│  │  except EmptyQueue:                                         │ │
│  │     pass                                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                 Server.handle_message()                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  try:                                                        │ │
│  │     1. Get handler from execute_task_hash_map               │ │
│  │     2. Execute command handler ──┐                          │ │
│  │                                   │ Exception?               │ │
│  │  except Exception as e: ←────────┘                          │ │
│  │     GlobalExceptionHandler.handle_message_exception(e)      │ │
│  │     Send RESP error to client                               │ │
│  │     return "Error: ..."                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│              GlobalExceptionHandler.handle_exception()           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  1. Extract exception type and message                      │ │
│  │  2. Build comprehensive error message                       │ │
│  │  3. Log full traceback to console                           │ │
│  │  4. Format RESP error response                              │ │
│  │  5. Send error to client via peer.send()                    │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT RECEIVES ERROR                         │
│              -ERR <Type> in <context>: <message>                │
└─────────────────────────────────────────────────────────────────┘
```

## Three-Layer Protection

```
┌───────────────────────────────────────────────────────────┐
│                      LAYER 1                              │
│              Command Parsing Protection                   │
│                   (Peer.read_loop)                        │
│  • RESP parsing errors                                    │
│  • Encoding/decoding errors                               │
│  • Invalid command format                                 │
└───────────────────────────────────────────────────────────┘
                         ↓
┌───────────────────────────────────────────────────────────┐
│                      LAYER 2                              │
│            Message Processing Protection                  │
│                   (Server.loop)                           │
│  • Message queue errors                                   │
│  • Message handling errors                                │
│  • Event loop errors                                      │
└───────────────────────────────────────────────────────────┘
                         ↓
┌───────────────────────────────────────────────────────────┐
│                      LAYER 3                              │
│            Command Execution Protection                   │
│                (Server.handle_message)                    │
│  • Database errors                                        │
│  • Business logic errors                                  │
│  • Data structure errors (KeyError, IndexError, etc.)     │
│  • Type errors, Value errors                              │
│  • Any unhandled exceptions                               │
└───────────────────────────────────────────────────────────┘
```

## Error Response Format

```
CLIENT COMMAND          SERVER EXCEPTION           CLIENT RESPONSE
──────────────          ────────────────           ───────────────
SET key abc      →      ValueError in             →  -ERR ValueError in
                        command execution             command execution:
                        (int conversion)              invalid literal...

GET missing_key  →      KeyError in               →  -ERR KeyError in
                        command execution             message processing:
                                                      'missing_key'

INVALID_CMD      →      Exception in              →  -ERR Exception in
                        parsing                       command parsing:
                                                      unknown command
```

## Console Logging Format

```
============================================================
GLOBAL EXCEPTION HANDLER - command execution (SetCommand)
============================================================
Exception Type: ValueError
Exception Message: invalid literal for int() with base 10
Traceback:
  File "server.py", line 123, in handle_message
    result = int(value)
ValueError: invalid literal for int() with base 10
============================================================
```

## Exception Categories Handled

1. **Parsing Exceptions**
   - RESP protocol errors
   - Encoding errors
   - Invalid command syntax

2. **Execution Exceptions**
   - ValueError, TypeError, KeyError
   - IndexError, AttributeError
   - ZeroDivisionError
   - Custom exceptions
   - Database exceptions

3. **System Exceptions**
   - ConnectionResetError
   - OSError
   - Socket errors
   - Queue errors

## Server Behavior

```
Before Global Exception Handler:
┌──────────────┐
│  Exception   │ → Server Crashes → Client Disconnected
└──────────────┘

After Global Exception Handler:
┌──────────────┐
│  Exception   │ → Caught & Logged → Error Sent → Server Continues
└──────────────┘                      to Client     Running Normally
```
