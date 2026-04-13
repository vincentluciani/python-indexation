"""Provide a gzip decompressor wrapper."""

import gzip


def get_decompressed_gzip_stream(raw_stream):
    """Return a decompressed gzip file object from a raw stream."""
    return gzip.GzipFile(fileobj=raw_stream)
