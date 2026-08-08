import pytest
from unittest.mock import Mock, patch, MagicMock
from vidara import (
    VidaraClient,
    UserInfo,
    StatsResult,
    UploadResult,
    RemoteUploadResult,
    VideoInfo,
    VideoListResult,
    CloneResult,
    FolderItem,
    VidaraAPIError,
    AuthenticationError,
)


def test_init_raises_value_error_if_no_key():
    with pytest.raises(ValueError):
        VidaraClient("")


def test_user_info_from_dict():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "premium": "expired",
        "premium_expire": "expired",
        "storage_left": "unlimited",
        "storage_used": 1024,
        "videos_total": 5,
    }
    user = UserInfo.from_dict(data)
    assert user.username == "testuser"
    assert user.storage_used == 1024
    assert user.videos_total == 5


def test_remote_upload_result_from_dict():
    data = {"filecode": "abc12345", "title": "test video", "size": 1000}
    res = RemoteUploadResult.from_dict(data)
    assert res.filecode == "abc12345"
    assert res.title == "test video"


def test_get_account_info(client, monkeypatch):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "status": 200,
        "msg": "OK",
        "result": {
            "username": "katso",
            "email": "katso@test.com",
            "premium": "expired",
            "premium_expire": "expired",
            "storage_left": "unlimited",
            "storage_used": 500,
            "videos_total": 10,
        },
    }
    monkeypatch.setattr(client.session, "get", lambda *args, **kwargs: mock_resp)

    info = client.get_account_info()
    assert info.username == "katso"
    assert info.videos_total == 10


def test_api_raises_auth_error_on_403(client, monkeypatch):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"status": 403, "msg": "access denied"}
    monkeypatch.setattr(client.session, "get", lambda *args, **kwargs: mock_resp)

    with pytest.raises(AuthenticationError):
        client.get_account_info()
