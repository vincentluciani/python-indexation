from src.extract_information.build_decompressor.build_decompressor import get_decompressor
from src.extract_information.build_parser.build_parser import get_parser

def parse_stream_from_file(parsing_args):
    decompressor = get_decompressor(parsing_args.get("decompressor", "none"))
    parser = get_parser(parsing_args.get("parser", "none"))
    with open(parsing_args.get("file_path"), "rb") as file:
        raw_stream = decompressor(file)
        yield from parser(raw_stream, parsing_args)

