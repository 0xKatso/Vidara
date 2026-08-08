"""Vidara API exceptions."""

from __future__ import annotations


class VidaraAPIError(Exception):
    """Base exception for all Vidara API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AuthenticationError(VidaraAPIError):
    """Invalid or missing API key."""


class NotFoundError(VidaraAPIError):
    """Resource not found."""


class EncodingError(VidaraAPIError):
    """Video encoding not completed."""


class RateLimitError(VidaraAPIError):
    """Too many requests."""


class BadRequestError(VidaraAPIError):
    """Invalid request parameters."""


class ServerError(VidaraAPIError):
    """Internal server error (5xx)."""
