"""Integration tests for sitemap ingestion and the local HTTP server."""

import os
import runpy
from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from ..test_server.local_http_server import LocalHttpServer


@pytest.fixture(scope="session")
def local_server_url():
    """Start a local HTTP server serving integration test fixtures."""
    fixtures_dir = Path(__file__).resolve().parents[1] / "test_server" / "fixtures"
    server = LocalHttpServer(directory=fixtures_dir, host="localhost", port=8001)
    server.start()
    yield server.url
    server.stop()


def test_scraper_against_local(local_server_url):
    """Verify the local HTTP server serves static files correctly."""
    target_url = f"{local_server_url}/test_page.html"

    response = requests.get(target_url, timeout=10)

    assert response.status_code == 200
    assert "Hello World" in response.text


def test_run_sitemap_to_elastic_parses_html_tables(local_server_url):
    """Verify sitemap parsing produces table rows and sends documents."""
    script_path = Path(__file__).resolve().parents[2] / "src" / "run_sitemap_to_elastic.py"
    sitemap_url = f"{local_server_url}/sitemap.xml.gz"

    with patch(
        "src.send_information.data_senders.send_data_to_elastic.send_list_of_documents_to_elastic"
    ) as mock_send:
        with patch.dict(os.environ, {"SITEMAP_URL": sitemap_url}, clear=False):
            runpy.run_path(str(script_path), run_name="__main__")

    mock_send.assert_called_once()
    sent_payload, index_name = mock_send.call_args[0]
    assert index_name == "vince"
    assert sent_payload == [
        {
            "category": "tutorial",
            "sub_category": "Tutorial Section",
            "question": "Question?",
            "answer": "Answer.",
        }
    ]


def test_run_sitemap_to_elastic_parses_multiple_tables_and_rows(local_server_url):
    """Verify sitemap parsing supports multiple tutorial tables and rows."""
    script_path = Path(__file__).resolve().parents[2] / "src" / "run_sitemap_to_elastic.py"
    sitemap_url = f"{local_server_url}/sitemap_multi.xml.gz"

    with patch(
        "src.send_information.data_senders.send_data_to_elastic.send_list_of_documents_to_elastic"
    ) as mock_send:
        with patch.dict(os.environ, {"SITEMAP_URL": sitemap_url}, clear=False):
            runpy.run_path(str(script_path), run_name="__main__")

    mock_send.assert_called_once()
    sent_payload, index_name = mock_send.call_args[0]
    assert index_name == "vince"
    assert sent_payload == [
        {
            "category": "tutorial",
            "sub_category": "Tutorial Section A",
            "question": "Question A1?",
            "answer": "Answer A1.",
        },
        {
            "category": "tutorial",
            "sub_category": "Tutorial Section A",
            "question": "Question A2?",
            "answer": "Answer A2.",
        },
        {
            "category": "tutorial",
            "sub_category": "Tutorial Section B",
            "question": "Question B1?",
            "answer": "Answer B1.",
        },
    ]
