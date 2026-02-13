

from parse_stream_from_url.build_decompressor.decompressors.gzip_decompressor import get_decompressed_gzip_stream
from parse_stream_from_url.build_decompressor.decompressors.zstd_decompressor import get_decompressed_zstd_stream


def build_decompressor(parser_name):
    registry = {
        "zstd": get_decompressed_zstd_stream,
        "gzip": get_decompressed_gzip_stream,
        "none": return_input
    }
    parser_class = registry.get(parser_name)
    return parser_class

def return_input(raw_stream):
    return raw_stream