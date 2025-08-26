from __future__ import annotations
from typing import Optional


class FiestaException(Exception):
    """Base exception for Fiesta"""
    pass


class LoginFailure(FiestaException):
    """Failed to login to Discord"""
    pass


class HTTPException(FiestaException):
    """HTTP request failed"""

    def __init__(self, status: int, message: str, code: Optional[int] = None):
        self.status: int = status
        self.message: str = message
        self.code: Optional[int] = code
        super().__init__(f"HTTP {status} (code {code}): {message}" if code else f"HTTP {status}: {message}")


class Forbidden(HTTPException):
    """403 Forbidden"""

    def __init__(self, message: str = "Forbidden", code: Optional[int] = None):
        super().__init__(403, message, code)


class NotFound(HTTPException):
    """404 Not Found"""

    def __init__(self, message: str = "Not found", code: Optional[int] = None):
        super().__init__(404, message, code)


class RateLimited(HTTPException):
    """429 Rate Limited"""

    def __init__(self, retry_after: float = 1.0, message: str = "Rate limited", code: Optional[int] = None):
        self.retry_after: float = retry_after
        super().__init__(429, f"{message} (retry after {retry_after}s)", code)


class ConnectionClosed(FiestaException):
    """WebSocket connection closed"""

    def __init__(self, code: int, reason: Optional[str] = None):
        self.code: int = code
        self.reason: Optional[str] = reason
        msg = f"WebSocket closed with code {code}" + (f" ({reason})" if reason else "")
        super().__init__(msg)


class GatewayError(FiestaException):
    """Gateway connection error"""
    pass


class CommandError(FiestaException):
    """Command execution error"""

    def __init__(self, command: str, message: str):
        self.command: str = command
        self.message: str = message
        super().__init__(f"Command '{command}' failed: {message}")
      
