import pytest
from unittest.mock import patch, MagicMock, mock_open
from extract_information.parse_stream_from_file import parse_stream_from_file


class TestParseStreamFromFile:
    @patch("extract_information.parse_stream_from_file.get_parser")
    @patch("extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_yields_parser_output(self, mock_file, mock_get_decompressor, mock_get_parser):
        mock_get_decompressor.return_value = MagicMock(return_value="decompressed_stream")
        mock_get_parser.return_value = MagicMock(return_value=iter(["item1", "item2"]))

        result = list(parse_stream_from_file("/fake/path.xml", "none", "xml", {}))

        assert result == ["item1", "item2"]

    @patch("extract_information.parse_stream_from_file.get_parser")
    @patch("extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_file_opened_in_binary_mode(self, mock_file, mock_get_decompressor, mock_get_parser):
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        list(parse_stream_from_file("/fake/path.xml", "none", "xml", {}))

        mock_file.assert_called_once_with("/fake/path.xml", "rb")

    @patch("extract_information.parse_stream_from_file.get_parser")
    @patch("extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_decompressor_called_with_file_handle(self, mock_file, mock_get_decompressor, mock_get_parser):
        fake_decompressor = MagicMock(return_value="decompressed_stream")
        mock_get_decompressor.return_value = fake_decompressor
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        list(parse_stream_from_file("/fake/path.xml", "gzip", "xml", {}))

        fake_decompressor.assert_called_once_with(mock_file.return_value.__enter__.return_value)

    @patch("extract_information.parse_stream_from_file.get_parser")
    @patch("extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_parser_called_with_decompressed_stream_and_parsing_args(
        self, mock_file, mock_get_decompressor, mock_get_parser
    ):
        mock_get_decompressor.return_value = MagicMock(return_value="decompressed_stream")
        fake_parser = MagicMock(return_value=iter([]))
        mock_get_parser.return_value = fake_parser

        parsing_args = {"parent_tag": "url", "child_tag": "loc"}
        list(parse_stream_from_file("/fake/path.xml", "none", "xml", parsing_args))

        fake_parser.assert_called_once_with("decompressed_stream", parsing_args)

    @patch("extract_information.parse_stream_from_file.get_parser")
    @patch("extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_correct_decompressor_and_parser_names_forwarded(
        self, mock_file, mock_get_decompressor, mock_get_parser
    ):
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        list(parse_stream_from_file("/fake/path.csv", "gzip", "csv", {}))

        mock_get_decompressor.assert_called_once_with("gzip")
        mock_get_parser.assert_called_once_with("csv")


class TestParseStreamFromFileErrors:
    @patch("extract_information.parse_stream_from_file.get_parser")
    @patch("extract_information.parse_stream_from_file.get_decompressor")
    def test_file_not_found_raises(self, mock_get_decompressor, mock_get_parser):
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        with pytest.raises(FileNotFoundError):
            list(parse_stream_from_file("/nonexistent/path.xml", "none", "xml", {}))

    @patch("extract_information.parse_stream_from_file.get_parser")
    @patch("extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", side_effect=PermissionError("denied"))
    def test_permission_error_raises(self, mock_file, mock_get_decompressor, mock_get_parser):
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        with pytest.raises(PermissionError):
            list(parse_stream_from_file("/protected/path.xml", "none", "xml", {}))


if __name__ == "__main__":
    pytest.main([__file__])
