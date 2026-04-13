import requests
from src.extract_information.build_decompressor.build_decompressor import get_decompressor
from src.extract_information.build_parser.build_parser import get_parser

def parse_stream_from_url(parsing_args):
    decompressor = get_decompressor(parsing_args.get("decompressor", "none"))
    parser = get_parser(parsing_args.get("parser", "none"))
    headers = {"User-Agent": "Mozilla/5.0"} 
    
    with requests.get(parsing_args.get("url"), stream=True, headers=headers) as r:
        r.raise_for_status()
        r.raw.decode_content = True 
        raw_stream =decompressor(r.raw)
        yield from parser(raw_stream, parsing_args)
