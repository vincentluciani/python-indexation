import pytest
from unittest.mock import patch, MagicMock
from src.extract_information.parse_stream_from_url import parse_stream_from_url


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_response(raw_content=b"data"):
    """Return a minimal mock that mimics a requests streaming response."""
    mock_response = MagicMock()
    mock_response.raw = MagicMock()
    mock_response.raw.decode_content = False
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)
    return mock_response


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------

class TestParseStreamFromUrl:
    @patch("src.extract_information.parse_stream_from_url.requests.get")
    @patch("src.extract_information.parse_stream_from_url.get_parser")
    @patch("src.extract_information.parse_stream_from_url.get_decompressor")
    def test_yields_parser_output(self, mock_get_decompressor, mock_get_parser, mock_requests_get):
        mock_response = _make_response()
        mock_requests_get.return_value = mock_response

        fake_decompressor = MagicMock(return_value="decompressed_stream")
        mock_get_decompressor.return_value = fake_decompressor

        fake_parser = MagicMock(return_value=iter(["item1", "item2"]))
        mock_get_parser.return_value = fake_parser

        result = list(parse_stream_from_url("http://example.com", "none", "xml", {}))

        assert result == ["item1", "item2"]

    @patch("src.extract_information.parse_stream_from_url.requests.get")
    @patch("src.extract_information.parse_stream_from_url.get_parser")
    @patch("src.extract_information.parse_stream_from_url.get_decompressor")
    def test_passes_url_and_headers_to_requests(self, mock_get_decompressor, mock_get_parser, mock_requests_get):
        mock_response = _make_response()
        mock_requests_get.return_value = mock_response
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        list(parse_stream_from_url("http://example.com/sitemap.xml", "none", "xml", {}))

        mock_requests_get.assert_called_once_with(
            "http://example.com/sitemap.xml",
            stream=True,
            headers={"User-Agent": "Mozilla/5.0"},
        )

    @patch("src.extract_information.parse_stream_from_url.requests.get")
    @patch("src.extract_information.parse_stream_from_url.get_parser")
    @patch("src.extract_information.parse_stream_from_url.get_decompressor")
    def test_decompressor_called_with_raw_stream(self, mock_get_decompressor, mock_get_parser, mock_requests_get):
        mock_response = _make_response()
        mock_requests_get.return_value = mock_response

        fake_decompressor = MagicMock(return_value="decompressed")
        mock_get_decompressor.return_value = fake_decompressor
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        list(parse_stream_from_url("http://example.com", "gzip", "xml", {}))

        fake_decompressor.assert_called_once_with(mock_response.raw)

    @patch("src.extract_information.parse_stream_from_url.requests.get")
    @patch("src.extract_information.parse_stream_from_url.get_parser")
    @patch("src.extract_information.parse_stream_from_url.get_decompressor")
    def test_parser_called_with_decompressed_stream_and_parsing_args(
        self, mock_get_decompressor, mock_get_parser, mock_requests_get
    ):
        mock_response = _make_response()
        mock_requests_get.return_value = mock_response

        mock_get_decompressor.return_value = MagicMock(return_value="decompressed_stream")
        fake_parser = MagicMock(return_value=iter([]))
        mock_get_parser.return_value = fake_parser

        parsing_args = {"parent_tag": "url", "child_tag": "loc"}
        list(parse_stream_from_url("http://example.com", "none", "xml", parsing_args))

        fake_parser.assert_called_once_with("decompressed_stream", parsing_args)

    @patch("src.extract_information.parse_stream_from_url.requests.get")
    @patch("src.extract_information.parse_stream_from_url.get_parser")
    @patch("src.extract_information.parse_stream_from_url.get_decompressor")
    def test_decode_content_set_to_true(self, mock_get_decompressor, mock_get_parser, mock_requests_get):
        mock_response = _make_response()
        mock_requests_get.return_value = mock_response
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        list(parse_stream_from_url("http://example.com", "none", "xml", {}))

        assert mock_response.raw.decode_content is True

    @patch("src.extract_information.parse_stream_from_url.requests.get")
    @patch("src.extract_information.parse_stream_from_url.get_parser")
    @patch("src.extract_information.parse_stream_from_url.get_decompressor")
    def test_correct_decompressor_and_parser_names_forwarded(
        self, mock_get_decompressor, mock_get_parser, mock_requests_get
    ):
        mock_response = _make_response()
        mock_requests_get.return_value = mock_response
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        list(parse_stream_from_url("http://example.com", "gzip", "csv", {}))

        mock_get_decompressor.assert_called_once_with("gzip")
        mock_get_parser.assert_called_once_with("csv")


# ---------------------------------------------------------------------------
# Error-path tests
# ---------------------------------------------------------------------------

class TestParseStreamFromUrlErrors:
    @patch("src.extract_information.parse_stream_from_url.requests.get")
    @patch("src.extract_information.parse_stream_from_url.get_parser")
    @patch("src.extract_information.parse_stream_from_url.get_decompressor")
    def test_http_error_raises(self, mock_get_decompressor, mock_get_parser, mock_requests_get):
        import requests as req
        mock_response = _make_response()
        mock_response.raise_for_status.side_effect = req.exceptions.HTTPError("404")
        mock_requests_get.return_value = mock_response
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        with pytest.raises(req.exceptions.HTTPError):
            list(parse_stream_from_url("http://example.com/missing", "none", "xml", {}))

    @patch("src.extract_information.parse_stream_from_url.requests.get")
    @patch("src.extract_information.parse_stream_from_url.get_parser")
    @patch("src.extract_information.parse_stream_from_url.get_decompressor")
    def test_connection_error_raises(self, mock_get_decompressor, mock_get_parser, mock_requests_get):
        import requests as req
        mock_requests_get.side_effect = req.exceptions.ConnectionError("unreachable")
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        with pytest.raises(req.exceptions.ConnectionError):
            list(parse_stream_from_url("http://unreachable.invalid", "none", "xml", {}))


if __name__ == "__main__":
    pytest.main([__file__])
