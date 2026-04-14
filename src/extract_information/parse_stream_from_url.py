"""Fetch and parse a remote stream from a URL."""

import requests
from src.extract_information.build_decompressor.build_decompressor import (
    get_decompressor,
)
from src.extract_information.build_parser.build_parser import get_parser


def parse_stream_from_url(parsing_args):
    """Yield parsed elements from a remote URL stream."""
    decompressor = get_decompressor(parsing_args.get("decompressor", "none"))
    parser = get_parser(parsing_args.get("parser", "none"))
    url = parsing_args.get("location")
    headers = {"User-Agent": "Mozilla/5.0"}
    print(f"Fetching and parsing stream from URL: {url}")

    with requests.get(
        url,
        stream=True,
        headers=headers,
        timeout=10,
    ) as r:
        r.raise_for_status()
        r.raw.decode_content = True
        raw_stream = decompressor(r.raw)
        yield from parser(raw_stream, parsing_args)
