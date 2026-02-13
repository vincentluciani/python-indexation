from extract_information.build_parser.parsers.xml_parser import parse_xml
from extract_information.build_parser.parsers.html_parser import parse_html_tables

def get_parser(parser_name):
    registry = {
        "xml": parse_xml,
        "html_tables": parse_html_tables,
        "none": return_input
    }
    parser_class = registry.get(parser_name)
    return parser_class

def return_input(raw_stream):
    return raw_stream