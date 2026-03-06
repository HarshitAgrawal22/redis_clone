"""
Global Exception Handler for Redis Clone
This module provides centralized exception handling functionality
to catch and respond to unhandled exceptions throughout the application.
"""

import traceback
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from python_redis.network.peer import Peer


class GlobalExceptionHandler:
    """Handles unhandled exceptions and sends proper error responses to clients"""

    @staticmethod
    def handle_exception(exception: Exception, peer: "Peer" = None, context: str = ""):
        """
        Handle an exception and send an error response to the client if peer is provided.
        
        Args:
            exception: The exception that occurred
            peer: The peer connection to send error response to (optional)
            context: Additional context about where the exception occurred
        
        Returns:
            str: Error message
        """
        # Get exception details
        error_type = type(exception).__name__
        error_message = str(exception)
        
        # Build comprehensive error message
        if context:
            full_error_msg = f"{error_type} in {context}: {error_message}"
        else:
            full_error_msg = f"{error_type}: {error_message}"
        
        # Log the full traceback for debugging
        print(f"\n{'='*60}")
        print(f"GLOBAL EXCEPTION HANDLER - {context}")
        print(f"{'='*60}")
        print(f"Exception Type: {error_type}")
        print(f"Exception Message: {error_message}")
        print(f"Traceback:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        # Send error response to client if peer is available
        if peer is not None:
            try:
                # Format error response in RESP protocol
                # error_response = RESP_Encoder.resp_error(f"{full_error_msg}")
                peer.socket_handler.send(full_error_msg, "e")
            except Exception as send_error:
                print(f"Failed to send error response to client: {send_error}")
        
        return full_error_msg

    @staticmethod
    def handle_command_exception(exception: Exception, peer: "Peer" = None, command_type: str = ""):
        """
        Handle exceptions during command execution.
        
        Args:
            exception: The exception that occurred
            peer: The peer connection
            command_type: The type of command being executed
        """
        context = f"command execution ({command_type})" if command_type else "command execution"
        return GlobalExceptionHandler.handle_exception(exception, peer, context)

    @staticmethod
    def handle_message_exception(exception: Exception, peer: "Peer" = None):
        """
        Handle exceptions during message processing.
        
        Args:
            exception: The exception that occurred
            peer: The peer connection
        """
        return GlobalExceptionHandler.handle_exception(exception, peer, "message processing")

    @staticmethod
    def handle_parsing_exception(exception: Exception, peer: "Peer" = None):
        """
        Handle exceptions during command parsing.
        
        Args:
            exception: The exception that occurred
            peer: The peer connection
        """
        return GlobalExceptionHandler.handle_exception(exception, peer, "command parsing")
