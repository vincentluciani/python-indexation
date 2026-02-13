import requests

def parse_stream_from_url(url, decompressor,parser,parsing_args):

    headers = {"User-Agent": "Mozilla/5.0"} 
    
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        r.raw.decode_content = True 
        raw_stream =decompressor(r.raw)
        yield from parser(raw_stream, parsing_args)
