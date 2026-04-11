import gzip
import pytest
from io import BytesIO
from src.extract_information.build_decompressor.build_decompressor import get_decompressor, return_input
from src.extract_information.build_decompressor.decompressors.gzip_decompressor import get_decompressed_gzip_stream


class TestGetDecompressor:
    def test_gzip_returns_gzip_function(self):
        result = get_decompressor("gzip")
        assert result is get_decompressed_gzip_stream

    def test_none_returns_passthrough_function(self):
        result = get_decompressor("none")
        assert result is return_input

    def test_unknown_name_returns_none(self):
        result = get_decompressor("unknown")
        assert result is None


class TestReturnInput:
    def test_returns_stream_unchanged(self):
        stream = BytesIO(b"some data")
        assert return_input(stream) is stream

    def test_returns_any_object_unchanged(self):
        obj = object()
        assert return_input(obj) is obj


class TestGetDecompressedGzipStream:
    def test_returns_gzip_file_object(self):
        data = BytesIO()
        with gzip.GzipFile(fileobj=data, mode="wb") as f:
            f.write(b"hello")
        data.seek(0)

        result = get_decompressed_gzip_stream(data)

        assert isinstance(result, gzip.GzipFile)

    def test_decompressed_content_is_readable(self):
        data = BytesIO()
        with gzip.GzipFile(fileobj=data, mode="wb") as f:
            f.write(b"hello world")
        data.seek(0)

        result = get_decompressed_gzip_stream(data)

        assert result.read() == b"hello world"


if __name__ == "__main__":
    pytest.main([__file__])
