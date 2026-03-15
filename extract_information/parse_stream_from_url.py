import requests
from extract_information.build_decompressor.build_decompressor import get_decompressor
from extract_information.build_parser.build_parser import get_parser

def parse_stream_from_url(url, decompressor_name, parser_name, parsing_args):
    decompressor = get_decompressor(decompressor_name)
    parser = get_parser(parser_name)
    headers = {"User-Agent": "Mozilla/5.0"} 
    
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        r.raw.decode_content = True 
        raw_stream =decompressor(r.raw)
        yield from parser(raw_stream, parsing_args)
