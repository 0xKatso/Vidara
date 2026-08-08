"""Async Vidara API client (requires httpx)."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from urllib.parse import urljoin

import httpx

from .exceptions import (
    VidaraAPIError,
    AuthenticationError,
    NotFoundError,
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


class AsyncVidaraClient:
    """Asynchronous Vidara API client.

    Requires the optional dependency: pip install vidara-api[async]
    """

    BASE_URL = "https://api.vidara.so/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.timeout = timeout

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        if params is None:
            params = {}
        params["api_key"] = self.api_key

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if method.upper() == "POST":
                resp = await client.post(url, params=params)
            else:
                resp = await client.get(url, params=params)

            try:
                resp.raise_for_status()
            except httpx.HTTPStatusError:
                raise VidaraAPIError(f"HTTP error: {resp.status_code}")

            result = resp.json()
            status = result.get("status")
            msg = result.get("msg", "Unknown error")

            if status == 200:
                return result.get("result") or result.get("data", {})
            elif status == 403:
                raise AuthenticationError(msg, status)
            elif status == 404:
                raise NotFoundError(msg, status)
            elif status >= 500:
                raise ServerError(msg, status)
            else:
                raise VidaraAPIError(msg, status)

    async def get_account_info(self) -> UserInfo:
        return UserInfo.from_dict(await self._request("GET", "/user/info"))

    async def get_account_stats(self, last: int = 7) -> StatsResult:
        return StatsResult.from_dict(
            await self._request("GET", "/user/stats", params={"last": last})
        )

    async def get_upload_server(self) -> str:
        data = await self._request("GET", "/upload/server")
        return data.get("upload_server", "")

    async def upload_from_url(self, url: str) -> RemoteUploadResult:
        return RemoteUploadResult.from_dict(
            await self._request("GET", "/upload/url", params={"url": url})
        )

    async def get_video_info(self, filecode: str) -> VideoInfo:
        data = await self._request("GET", "/video/info", params={"filecode": filecode})
        if isinstance(data, list):
            data = data[0] if data else {}
        return VideoInfo.from_dict(data)

    async def list_videos(
        self,
        page: int = 1,
        limit: int = 100,
        title: Optional[str] = None,
        folder_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> VideoListResult:
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if title is not None:
            params["title"] = title
        if folder_id is not None:
            params["fld_id"] = folder_id
        if status is not None:
            params["status"] = status
        return VideoListResult.from_dict(
            await self._request("GET", "/video/list", params=params)
        )

    async def clone_video(self, filecode: str) -> CloneResult:
        return CloneResult.from_dict(
            await self._request("GET", "/video/clone", params={"filecode": filecode})
        )

    async def get_encoding_status(self, filecode: str) -> List[EncodingProgress]:
        data = await self._request("GET", "/video/status", params={"filecode": filecode})
        encodings = data.get("encodings") or []
        return [EncodingProgress.from_dict(e) for e in encodings]

    async def rename_video(self, filecode: str, title: str) -> None:
        await self._request(
            "GET", "/video/rename", params={"filecode": filecode, "title": title}
        )

    async def move_video(self, filecode: str, folder_id: int = 0) -> None:
        await self._request(
            "GET", "/video/move", params={"filecode": filecode, "fld_id": folder_id}
        )

    async def delete_video(self, filecode: str) -> None:
        await self._request("GET", "/video/delete", params={"filecode": filecode})

    async def get_deleted_files(self, limit: int = 50) -> List[DeletedFile]:
        data = await self._request("GET", "/video/deleted", params={"limit": limit})
        return [DeletedFile.from_dict(f) for f in data.get("files", [])]

    async def get_dmca_reports(self) -> List[DMCAReport]:
        data = await self._request("GET", "/video/dmca")
        return [DMCAReport.from_dict(f) for f in data.get("files", [])]

    async def list_folders(self) -> List[FolderItem]:
        data = await self._request("GET", "/folder/list")
        return [FolderItem.from_dict(f) for f in data.get("folders", [])]

    async def create_folder(self, name: str) -> FolderItem:
        return FolderItem.from_dict(
            await self._request("GET", "/folder/create", params={"name": name})
        )

    async def rename_folder(self, folder_id: int, name: str) -> None:
        await self._request(
            "GET", "/folder/edit", params={"fld_id": folder_id, "name": name}
        )

    async def delete_folder(self, folder_id: int) -> None:
        await self._request("GET", "/folder/delete", params={"fld_id": folder_id})
