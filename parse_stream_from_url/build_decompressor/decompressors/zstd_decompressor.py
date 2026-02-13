
import zstandard as zstd  # pip install zstandard

def get_decompressed_zstd_stream(raw_stream):
    dctx = zstd.ZstdDecompressor()
    return dctx.stream_reader(raw_stream)