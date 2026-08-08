"""Dataclasses representing Vidara API responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class UserInfo:
    username: str
    email: str
    premium: str
    premium_expire: str
    storage_left: str
    storage_used: int
    videos_total: int

    @classmethod
    def from_dict(cls, data: dict) -> UserInfo:
        return cls(
            username=data.get("username", ""),
            email=data.get("email", ""),
            premium=data.get("premium", ""),
            premium_expire=data.get("premium_expire", ""),
            storage_left=data.get("storage_left", ""),
            storage_used=data.get("storage_used", 0),
            videos_total=data.get("videos_total", 0),
        )


@dataclass
class AccountStat:
    day: str
    views: int
    earnings: str

    @classmethod
    def from_dict(cls, data: dict) -> AccountStat:
        return cls(
            day=data.get("day", ""),
            views=data.get("views", 0),
            earnings=data.get("earnings", "0"),
        )


@dataclass
class StatsResult:
    stats: List[AccountStat]
    results: int
    days: int

    @classmethod
    def from_dict(cls, data: dict) -> StatsResult:
        return cls(
            stats=[AccountStat.from_dict(s) for s in data.get("stats", [])],
            results=data.get("results", 0),
            days=data.get("days", 0),
        )


@dataclass
class UploadResult:
    url: str
    title: str
    video_id: int
    filecode: str

    @classmethod
    def from_dict(cls, data: dict) -> UploadResult:
        return cls(
            url=data.get("url", ""),
            title=data.get("title", ""),
            video_id=data.get("video_id", 0),
            filecode=data.get("filecode", ""),
        )


@dataclass
class RemoteUploadResult:
    filecode: str
    title: str
    size: int

    @classmethod
    def from_dict(cls, data: dict) -> RemoteUploadResult:
        return cls(
            filecode=data.get("filecode", ""),
            title=data.get("title", ""),
            size=data.get("size", 0),
        )


@dataclass
class VideoInfo:
    filecode: str
    status: str
    player_img: Optional[str] = None
    link: Optional[str] = None
    video_length: Optional[str] = None
    video_title: Optional[str] = None
    video_views: Optional[int] = None
    video_created: Optional[str] = None
    file_active: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> VideoInfo:
        return cls(
            filecode=data.get("filecode", ""),
            status=data.get("status", ""),
            player_img=data.get("player_img"),
            link=data.get("link"),
            video_length=data.get("video_length"),
            video_title=data.get("video_title"),
            video_views=data.get("video_views"),
            video_created=data.get("video_created"),
            file_active=data.get("file_active"),
        )


@dataclass
class VideoItem:
    vid_id: int
    filecode: str
    title: str
    thumbnail: str
    length: str
    link: str
    views: int
    uploaded: str
    status: str
    file_active: int

    @classmethod
    def from_dict(cls, data: dict) -> VideoItem:
        return cls(
            vid_id=data.get("vid_id", 0),
            filecode=data.get("filecode", ""),
            title=data.get("title", ""),
            thumbnail=data.get("thumbnail", ""),
            length=data.get("length", ""),
            link=data.get("link", ""),
            views=data.get("views", 0),
            uploaded=data.get("uploaded", ""),
            status=data.get("status", ""),
            file_active=data.get("file_active", 1),
        )


@dataclass
class VideoListResult:
    videos: List[VideoItem]
    results: int
    page: int
    per_page: int
    total_pages: int
    total: int

    @classmethod
    def from_dict(cls, data: dict) -> VideoListResult:
        return cls(
            videos=[VideoItem.from_dict(v) for v in data.get("videos", [])],
            results=data.get("results", 0),
            page=data.get("page", 1),
            per_page=data.get("per_page", 100),
            total_pages=data.get("total_pages", 1),
            total=data.get("total", 0),
        )


@dataclass
class CloneResult:
    url: str
    filecode: str

    @classmethod
    def from_dict(cls, data: dict) -> CloneResult:
        return cls(
            url=data.get("url", ""),
            filecode=data.get("filecode", ""),
        )


@dataclass
class EncodingProgress:
    filecode: str
    type: str
    progress_percentage: str
    last_update: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> EncodingProgress:
        return cls(
            filecode=data.get("filecode", ""),
            type=data.get("type", ""),
            progress_percentage=data.get("progress_percentage", "0%"),
            last_update=data.get("last_update", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class FolderItem:
    fld_id: int
    name: str
    code: int
    videos: int
    created: str

    @classmethod
    def from_dict(cls, data: dict) -> FolderItem:
        return cls(
            fld_id=data.get("fld_id", 0),
            name=data.get("name", ""),
            code=data.get("code", 0),
            videos=data.get("videos", 0),
            created=data.get("created", ""),
        )


@dataclass
class DeletedFile:
    filecode: str
    title: str
    deleted: str

    @classmethod
    def from_dict(cls, data: dict) -> DeletedFile:
        return cls(
            filecode=data.get("filecode", ""),
            title=data.get("title", ""),
            deleted=data.get("deleted", ""),
        )


@dataclass
class DMCAReport:
    filecode: str
    title: str
    date: str

    @classmethod
    def from_dict(cls, data: dict) -> DMCAReport:
        return cls(
            filecode=data.get("filecode", ""),
            title=data.get("title", ""),
            date=data.get("date", ""),
        )
