
def parse_stream_from_file(file_path, decompressor, parser, parsing_args):
    with open(file_path, "rb") as file:
        raw_stream = decompressor(file)
        yield from parser(raw_stream, parsing_args)

