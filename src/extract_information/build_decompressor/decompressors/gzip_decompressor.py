import gzip

def get_decompressed_gzip_stream(raw_stream):
    return gzip.GzipFile(fileobj=raw_stream)

