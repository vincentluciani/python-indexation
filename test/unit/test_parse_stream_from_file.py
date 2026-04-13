import pytest
from unittest.mock import patch, MagicMock, mock_open
from src.extract_information.parse_stream_from_file import parse_stream_from_file


class TestParseStreamFromFile:
    @patch("src.extract_information.parse_stream_from_file.get_parser")
    @patch("src.extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_yields_parser_output(self, mock_file, mock_get_decompressor, mock_get_parser):
        mock_get_decompressor.return_value = MagicMock(return_value="decompressed_stream")
        mock_get_parser.return_value = MagicMock(return_value=iter(["item1", "item2"]))

        parsing_args = {
            "file_path": "/fake/path.xml",
            "decompressor": "none",
            "parser": "xml",
        }
        result = list(parse_stream_from_file(parsing_args))

        assert result == ["item1", "item2"]

    @patch("src.extract_information.parse_stream_from_file.get_parser")
    @patch("src.extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_file_opened_in_binary_mode(self, mock_file, mock_get_decompressor, mock_get_parser):
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        parsing_args = {
            "file_path": "/fake/path.xml",
            "decompressor": "none",
            "parser": "xml",
        }
        list(parse_stream_from_file(parsing_args))

        mock_file.assert_called_once_with("/fake/path.xml", "rb")

    @patch("src.extract_information.parse_stream_from_file.get_parser")
    @patch("src.extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_decompressor_called_with_file_handle(self, mock_file, mock_get_decompressor, mock_get_parser):
        fake_decompressor = MagicMock(return_value="decompressed_stream")
        mock_get_decompressor.return_value = fake_decompressor
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        parsing_args = {
            "file_path": "/fake/path.xml",
            "decompressor": "gzip",
            "parser": "xml",
        }
        list(parse_stream_from_file(parsing_args))

        fake_decompressor.assert_called_once_with(mock_file.return_value.__enter__.return_value)

    @patch("src.extract_information.parse_stream_from_file.get_parser")
    @patch("src.extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_parser_called_with_decompressed_stream_and_parsing_args(
        self, mock_file, mock_get_decompressor, mock_get_parser
    ):
        mock_get_decompressor.return_value = MagicMock(return_value="decompressed_stream")
        fake_parser = MagicMock(return_value=iter([]))
        mock_get_parser.return_value = fake_parser

        parsing_args = {
            "file_path": "/fake/path.xml",
            "decompressor": "none",
            "parser": "xml",
            "parent_tag": "url",
            "child_tag": "loc",
        }
        list(parse_stream_from_file(parsing_args))

        fake_parser.assert_called_once_with("decompressed_stream", parsing_args)

    @patch("src.extract_information.parse_stream_from_file.get_parser")
    @patch("src.extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", new_callable=mock_open, read_data=b"data")
    def test_correct_decompressor_and_parser_names_forwarded(
        self, mock_file, mock_get_decompressor, mock_get_parser
    ):
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        parsing_args = {
            "file_path": "/fake/path.csv",
            "decompressor": "gzip",
            "parser": "csv",
        }
        list(parse_stream_from_file(parsing_args))

        mock_get_decompressor.assert_called_once_with("gzip")
        mock_get_parser.assert_called_once_with("csv")


class TestParseStreamFromFileErrors:
    @patch("src.extract_information.parse_stream_from_file.get_parser")
    @patch("src.extract_information.parse_stream_from_file.get_decompressor")
    def test_file_not_found_raises(self, mock_get_decompressor, mock_get_parser):
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        with pytest.raises(FileNotFoundError):
            parsing_args = {
                "file_path": "/nonexistent/path.xml",
                "decompressor": "none",
                "parser": "xml",
            }
            list(parse_stream_from_file(parsing_args))

    @patch("src.extract_information.parse_stream_from_file.get_parser")
    @patch("src.extract_information.parse_stream_from_file.get_decompressor")
    @patch("builtins.open", side_effect=PermissionError("denied"))
    def test_permission_error_raises(self, mock_file, mock_get_decompressor, mock_get_parser):
        mock_get_decompressor.return_value = MagicMock(return_value="stream")
        mock_get_parser.return_value = MagicMock(return_value=iter([]))

        with pytest.raises(PermissionError):
            parsing_args = {
                "file_path": "/protected/path.xml",
                "decompressor": "none",
                "parser": "xml",
            }
            list(parse_stream_from_file(parsing_args))


if __name__ == "__main__":
    pytest.main([__file__])
