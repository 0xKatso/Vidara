"""Core Vidara API client."""

from __future__ import annotations

from typing import Optional, List, Dict, Any
from urllib.parse import urljoin

import requests

from .exceptions import (
    VidaraAPIError,
    AuthenticationError,
    NotFoundError,
    EncodingError,
    BadRequestError,
    ServerError,
)
from .models import (
    UserInfo,
    StatsResult,
    UploadResult,
    RemoteUploadResult,
    VideoInfo,
    VideoListResult,
    CloneResult,
    EncodingProgress,
    FolderItem,
    DeletedFile,
    DMCAReport,
)


class VidaraClient:
    """Synchronous Vidara API client."""

    BASE_URL = "https://api.vidara.so/v1"
    UPLOAD_URL = "https://s1.vidara.so/api/upload"

    def __init__(self, api_key: str, timeout: int = 30):
        """Initialize client with API key.

        Args:
            api_key: Your Vidara API key from https://vidara.to/settings
            timeout: Request timeout in seconds (default: 30)
        """
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to API.

        Args:
            method: HTTP method (GET, POST, etc)
            endpoint: API endpoint path
            params: Query parameters
            data: Form data
            files: Files for multipart upload

        Returns:
            Parsed JSON response

        Raises:
            VidaraAPIError: On API errors
        """
        url = f"{self.BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        if params is None:
            params = {}
        params["api_key"] = self.api_key

        try:
            if method.upper() == "POST":
                resp = self.session.post(
                    url,
                    params=params,
                    data=data,
                    files=files,
                    timeout=self.timeout,
                )
            else:
                resp = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                )

            resp.raise_for_status()
            result = resp.json()

            # Check API response status
            status = result.get("status")
            msg = result.get("msg", "Unknown error")

            if status == 200:
                return result.get("result") or result.get("data", {})
            elif status == 403:
                raise AuthenticationError(msg, status)
            elif status == 404:
                raise NotFoundError(msg, status)
            elif status == 429:
                raise ServerError("Rate limited", status)
            elif status >= 500:
                raise ServerError(msg, status)
            else:
                raise VidaraAPIError(msg, status)

        except requests.RequestException as e:
            raise VidaraAPIError(f"Request failed: {str(e)}")

    def get_account_info(self) -> UserInfo:
        """Get account info.

        Returns:
            UserInfo with account details
        """
        data = self._request("GET", "/user/info")
        return UserInfo.from_dict(data)

    def get_account_stats(self, last: int = 7) -> StatsResult:
        """Get per-day views and earnings.

        Args:
            last: Number of days to report (1-365, default: 7)

        Returns:
            StatsResult with daily stats
        """
        data = self._request("GET", "/user/stats", params={"last": last})
        return StatsResult.from_dict(data)

    def get_upload_server(self) -> str:
        """Get upload server URL.

        Returns:
            Upload server URL
        """
        data = self._request("GET", "/upload/server")
        return data.get("upload_server", "")

    def upload_file(self, file_path: str) -> UploadResult:
        """Upload video file.

        Args:
            file_path: Path to local video file

        Returns:
            UploadResult with new video info
        """
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                data = self._request(
                    "POST",
                    "/upload",
                    files=files,
                )
            return UploadResult.from_dict(data)
        except FileNotFoundError:
            raise BadRequestError(f"File not found: {file_path}")

    def upload_from_url(self, url: str) -> RemoteUploadResult:
        """Upload video from URL.

        Args:
            url: Direct URL to video file or Vidara link

        Returns:
            RemoteUploadResult with upload info
        """
        data = self._request("GET", "/upload/url", params={"url": url})
        return RemoteUploadResult.from_dict(data)

    def upload_thumbnail(self, filecode: str, thumb_url: str) -> None:
        """Upload custom thumbnail for video.

        Args:
            filecode: Video filecode
            thumb_url: Direct URL to thumbnail image (jpg, png, gif, webp)
        """
        self._request(
            "GET",
            "/upload/thumb",
            params={"filecode": filecode, "thumb_url": thumb_url},
        )

    def upload_subtitle(self, filecode: str, sub_lang: str, sub_url: str) -> None:
        """Upload subtitle for video.

        Args:
            filecode: Video filecode
            sub_lang: Subtitle language (e.g., 'English')
            sub_url: Direct URL to SRT or VTT file
        """
        self._request(
            "GET",
            "/upload/sub",
            params={
                "filecode": filecode,
                "sub_lang": sub_lang,
                "sub_url": sub_url,
            },
        )

    # ── File / Video ──────────────────────────────────────────────────────

    def get_video_info(self, filecode: str) -> VideoInfo:
        """Get video info.

        Args:
            filecode: Video filecode

        Returns:
            VideoInfo for the video
        """
        data = self._request("GET", "/video/info", params={"filecode": filecode})
        # API returns a list; first element is the primary record
        if isinstance(data, list):
            data = data[0] if data else {}
        return VideoInfo.from_dict(data)

    def list_videos(
        self,
        page: int = 1,
        limit: int = 100,
        title: Optional[str] = None,
        folder_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> VideoListResult:
        """List videos in your account.

        Args:
            page: Page number (starts from 1)
            limit: Results per page (max 200)
            title: Filter by title (partial match)
            folder_id: Filter by folder ID
            status: Filter by status: active, blocked, error

        Returns:
            VideoListResult with paginated video list
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if title is not None:
            params["title"] = title
        if folder_id is not None:
            params["fld_id"] = folder_id
        if status is not None:
            params["status"] = status
        data = self._request("GET", "/video/list", params=params)
        return VideoListResult.from_dict(data)

    def clone_video(self, filecode: str) -> CloneResult:
        """Clone a video.

        Args:
            filecode: Source video filecode (must be your own)

        Returns:
            CloneResult with new filecode and URL
        """
        data = self._request("GET", "/video/clone", params={"filecode": filecode})
        return CloneResult.from_dict(data)

    def get_encoding_status(self, filecode: str) -> List[EncodingProgress]:
        """Check encoding progress for a video.

        Args:
            filecode: Video filecode

        Returns:
            List of EncodingProgress objects (empty if nothing in progress)
        """
        data = self._request("GET", "/video/status", params={"filecode": filecode})
        encodings = data.get("encodings") or []
        return [EncodingProgress.from_dict(e) for e in encodings]

    def rename_video(self, filecode: str, title: str) -> None:
        """Rename a video.

        Args:
            filecode: Video filecode
            title: New title (must not be empty)
        """
        self._request(
            "GET",
            "/video/rename",
            params={"filecode": filecode, "title": title},
        )

    def move_video(self, filecode: str, folder_id: int = 0) -> None:
        """Move video to a folder.

        Args:
            filecode: Video filecode
            folder_id: Destination folder ID (0 = root)
        """
        self._request(
            "GET",
            "/video/move",
            params={"filecode": filecode, "fld_id": folder_id},
        )

    def delete_video(self, filecode: str) -> None:
        """Soft-delete a video.

        Args:
            filecode: Video filecode
        """
        self._request("GET", "/video/delete", params={"filecode": filecode})

    def get_deleted_files(self, limit: int = 50) -> List[DeletedFile]:
        """List your deleted videos.

        Args:
            limit: Number of results (max 500, default 50)

        Returns:
            List of DeletedFile objects
        """
        data = self._request("GET", "/video/deleted", params={"limit": limit})
        files = data.get("files", [])
        return [DeletedFile.from_dict(f) for f in files]

    def get_dmca_reports(self) -> List[DMCAReport]:
        """List videos with upheld DMCA reports.

        Returns:
            List of DMCAReport objects
        """
        data = self._request("GET", "/video/dmca")
        files = data.get("files", [])
        return [DMCAReport.from_dict(f) for f in files]

    # ── Folders ───────────────────────────────────────────────────────────

    def list_folders(self) -> List[FolderItem]:
        """List all your folders.

        Returns:
            List of FolderItem objects
        """
        data = self._request("GET", "/folder/list")
        folders = data.get("folders", [])
        return [FolderItem.from_dict(f) for f in folders]

    def create_folder(self, name: str) -> FolderItem:
        """Create a new folder.

        Args:
            name: Folder name

        Returns:
            FolderItem for the created folder
        """
        data = self._request("GET", "/folder/create", params={"name": name})
        return FolderItem.from_dict(data)

    def rename_folder(self, folder_id: int, name: str) -> None:
        """Rename a folder.

        Args:
            folder_id: Folder ID
            name: New folder name
        """
        self._request(
            "GET",
            "/folder/edit",
            params={"fld_id": folder_id, "name": name},
        )

    def delete_folder(self, folder_id: int) -> None:
        """Delete a folder.

        Videos inside are moved to root.

        Args:
            folder_id: Folder ID
        """
        self._request("GET", "/folder/delete", params={"fld_id": folder_id})

    # ── Upload from URL (alias) ───────────────────────────────────────────

    def upload_url(self, url: str) -> RemoteUploadResult:
        """Alias for upload_from_url.

        Args:
            url: Direct URL to video or Vidara link

        Returns:
            RemoteUploadResult
        """
        return self.upload_from_url(url)
