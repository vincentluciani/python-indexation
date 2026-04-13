"""Build parser functions for supported formats."""

from src.extract_information.build_parser.parsers.html_parser import (
    parse_html_tables_with_titles,
)
from src.extract_information.build_parser.parsers.csv_parser import parse_csv
from src.extract_information.build_parser.parsers.xml_parser import parse_xml


def get_parser(parser_name):
    """Return the parser function matching the configured name."""
    registry = {
        "xml": parse_xml,
        "html_tables": parse_html_tables_with_titles,
        "csv": parse_csv,
        "none": return_input,
    }
    parser_function = registry.get(parser_name)
    return parser_function


def return_input(raw_stream):
    """Return the input stream unchanged."""
    return raw_stream
