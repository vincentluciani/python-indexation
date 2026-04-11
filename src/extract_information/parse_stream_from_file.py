from src.extract_information.build_decompressor.build_decompressor import get_decompressor
from src.extract_information.build_parser.build_parser import get_parser

def parse_stream_from_file(file_path, decompressor_name, parser_name, parsing_args):
    decompressor = get_decompressor(decompressor_name)
    parser = get_parser(parser_name)
    with open(file_path, "rb") as file:
        raw_stream = decompressor(file)
        yield from parser(raw_stream, parsing_args)

