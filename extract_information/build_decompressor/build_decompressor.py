from extract_information.build_decompressor.decompressors.gzip_decompressor import get_decompressed_gzip_stream

def get_decompressor(parser_name):
    registry = {
        "gzip": get_decompressed_gzip_stream,
        "none": return_input
    }
    parser_class = registry.get(parser_name)
    return parser_class

def return_input(raw_stream):
    return raw_stream