import io
from lxml import etree
import requests
import xml.etree.ElementTree as ET

import zstandard as zstd

from parse_stream_from_url.build_decompressor.build_decompressor import build_decompressor  # pip install zstandard


def parse_xml_stream_from_url(url, parent_tag="url", child_tag="loc"):

    headers = {"User-Agent": "Mozilla/5.0","Accept-Encoding": "identity"} 
    NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        r.raw.decode_content = True 
        decompressor = build_decompressor('gzip')
        raw_stream =decompressor(r.raw)

        context = etree.iterparse(raw_stream, events=("end",), tag=f"{{{NS['ns']}}}{parent_tag}")
        
        for _, elem in context:
            child = elem.find(f"ns:{child_tag}", NS)
            if child is not None and child.text:
                yield child.text.strip()
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
