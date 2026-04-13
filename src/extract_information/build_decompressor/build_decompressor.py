"""Build decompressor functions for supported stream formats."""

from src.extract_information.build_decompressor.decompressors.gzip_decompressor import (
    get_decompressed_gzip_stream,
)


def get_decompressor(decompressor_name):
    """Return the decompressor function matching the configured name."""
    registry = {
        "gzip": get_decompressed_gzip_stream,
        "none": return_input,
    }
    decompressor_function = registry.get(decompressor_name)
    return decompressor_function


def return_input(raw_stream):
    """Return the input stream unchanged."""
    return raw_stream
