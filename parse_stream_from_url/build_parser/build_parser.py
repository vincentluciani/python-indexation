def build_decompressor(parser_name):
    registry = {
        "xml": parse_xml,
        "none": return_input
    }
    parser_class = registry.get(parser_name)
    return parser_class

def return_input(raw_stream):
    return raw_stream