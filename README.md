# vidara-api

[![PyPI version](https://img.shields.io/pypi/v/vidara-api.svg)](https://pypi.org/project/vidara-api/)
[![Python Versions](https://img.shields.io/pypi/pyversions/vidara-api.svg)](https://pypi.org/project/vidara-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional, fully type-hinted Python SDK and API wrapper for the [Vidara](https://vidara.to) video hosting API. Available officially on PyPI as [`vidara-api`](https://pypi.org/project/vidara-api/).

> **Unofficial.** Not affiliated with Vidara. Interoperable with `https://api.vidara.so/v1`.

## PyPI Package

Published to PyPI: https://pypi.org/project/vidara-api/

```bash
pip install vidara-api            # sync only
pip install vidara-api[async]     # with async support
```

## Features

- ✅ **Published on PyPI** as [`vidara-api`](https://pypi.org/project/vidara-api/)
- ✅ **Sync** client built on `requests`
- ✅ **Async** client built on `httpx`
- ✅ **Fully typed** dataclass models + `py.typed` (PEP 561)
- ✅ **Clear exceptions** for auth, not-found, server errors
- ✅ Covers **every** documented endpoint: account, upload, video/file, folders
- ✅ Zero-config; just your API key

## Quickstart

```python
from vidara import VidaraClient

# Grab your API key at https://vidara.to/settings
client = VidaraClient("YOUR_API_KEY")

# Account info
me = client.get_account_info()
print(me.username, me.videos_total)

# Upload a video from a URL
video = client.upload_from_url("https://example.com/video.mp4")
print(video.filecode, video.title)

# List your videos
videos = client.list_videos(limit=50)
for v in videos.videos:
    print(v.title, v.link)

# Rename a video
client.rename_video(video.filecode, "My New Title")

# Move to a folder
client.move_video(video.filecode, folder_id=5)
```

## Async usage

```python
import asyncio
from vidara import AsyncVidaraClient

async def main():
    client = AsyncVidaraClient("YOUR_API_KEY")
    me = await client.get_account_info()
    print(me.username)

asyncio.run(main())
```

## Endpoints

| Area     | Methods                                                          |
|----------|------------------------------------------------------------------|
| Account  | `get_account_info`, `get_account_stats`                          |
| Upload   | `get_upload_server`, `upload_file`, `upload_from_url`, `upload_thumbnail`, `upload_subtitle` |
| Files    | `get_video_info`, `list_videos`, `clone_video`, `get_encoding_status`, `rename_video`, `move_video`, `delete_video`, `get_deleted_files`, `get_dmca_reports` |
| Folders  | `list_folders`, `create_folder`, `rename_folder`, `delete_folder` |

## Error handling

All API errors raise a `VidaraAPIError` (or a subclass):

- `AuthenticationError` — invalid/forbidden API key (403)
- `NotFoundError` — resource missing (404)
- `ServerError` — server failure (5xx)
- `BadRequestError` — bad input
- `EncodingError` — video still encoding
- `RateLimitError` — too many requests

```python
from vidara import VidaraClient, VidaraAPIError

client = VidaraClient("bad_key")
try:
    client.get_account_info()
except VidaraAPIError as e:
    print(e)  # access denied
```

## Development

```bash
pip install -e .[dev]
pytest
```

## License

[MIT](LICENSE) © 2026 0xKatso
