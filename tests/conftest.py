"""Tests for vidara package."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json


@pytest.fixture
def api_key():
    """Test API key."""
    return "test_api_key_12345"


@pytest.fixture
def mock_response():
    """Mock requests.Response object."""
    response = Mock()
    response.status_code = 200
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def client(api_key):
    """Create test client."""
    from vidara import VidaraClient
    return VidaraClient(api_key, timeout=10)


@pytest.fixture
def mock_session(monkeypatch):
    """Mock requests.Session."""
    mock = Mock()
    monkeypatch.setattr("vidara.client.requests.Session", lambda: mock)
    return mock
