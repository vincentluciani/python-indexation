import io
from lxml import etree
import requests
import xml.etree.ElementTree as ET

import zstandard as zstd
from parse_stream_from_url.build_parser.build_parser import build_parser

from parse_stream_from_url.build_decompressor.build_decompressor import build_decompressor  # pip install zstandard


def parse_xml_stream_from_url(url, parent_tag="url", child_tag="loc"):

    headers = {"User-Agent": "Mozilla/5.0","Accept-Encoding": "identity"} 
    
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        r.raw.decode_content = True 
        decompressor = build_decompressor('gzip')
        raw_stream =decompressor(r.raw)

        parser = build_parser('xml')

        yield from parser(raw_stream, parent_tag, child_tag)
