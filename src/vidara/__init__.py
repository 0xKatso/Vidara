"""vidara-api: A Python wrapper for the Vidara video hosting API.

Example:
    >>> from vidara import VidaraClient
    >>> client = VidaraClient("your_api_key")
    >>> info = client.get_account_info()
    >>> print(info.username)
"""

from .client import VidaraClient
from .models import (
    UserInfo,
    StatsResult,
    AccountStat,
    UploadResult,
    RemoteUploadResult,
    VideoInfo,
    VideoItem,
    VideoListResult,
    CloneResult,
    EncodingProgress,
    FolderItem,
    DeletedFile,
    DMCAReport,
)
from .exceptions import (
    VidaraAPIError,
    AuthenticationError,
    NotFoundError,
    EncodingError,
    RateLimitError,
    BadRequestError,
    ServerError,
)

try:  # pragma: no cover - optional dependency
    from .async_client import AsyncVidaraClient

    __all__ = [
        "VidaraClient",
        "AsyncVidaraClient",
        "UserInfo",
        "StatsResult",
        "AccountStat",
        "UploadResult",
        "RemoteUploadResult",
        "VideoInfo",
        "VideoItem",
        "VideoListResult",
        "CloneResult",
        "EncodingProgress",
        "FolderItem",
        "DeletedFile",
        "DMCAReport",
        "VidaraAPIError",
        "AuthenticationError",
        "NotFoundError",
        "EncodingError",
        "RateLimitError",
        "BadRequestError",
        "ServerError",
    ]
except ImportError:  # pragma: no cover
    __all__ = [
        "VidaraClient",
        "UserInfo",
        "StatsResult",
        "AccountStat",
        "UploadResult",
        "RemoteUploadResult",
        "VideoInfo",
        "VideoItem",
        "VideoListResult",
        "CloneResult",
        "EncodingProgress",
        "FolderItem",
        "DeletedFile",
        "DMCAReport",
        "VidaraAPIError",
        "AuthenticationError",
        "NotFoundError",
        "EncodingError",
        "RateLimitError",
        "BadRequestError",
        "ServerError",
    ]


__version__ = "0.1.0"
