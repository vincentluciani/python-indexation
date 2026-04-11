import pytest
from src.extract_information.build_parser.build_parser import get_parser, return_input
from src.extract_information.build_parser.parsers.xml_parser import parse_xml
from src.extract_information.build_parser.parsers.html_parser import parse_html_tables_with_titles
from src.extract_information.build_parser.parsers.csv_parser import parse_csv


def test_xml_returns_parse_xml():
    assert get_parser("xml") is parse_xml

def test_html_tables_returns_parse_html():
    assert get_parser("html_tables") is parse_html_tables_with_titles

def test_csv_returns_parse_csv():
    assert get_parser("csv") is parse_csv

def test_none_returns_return_input():
    assert get_parser("none") is return_input

def test_unknown_name_returns_none():
    assert get_parser("unknown") is None

def test_empty_string_returns_none():
    assert get_parser("") is None

def test_case_sensitive():
    # Registry keys are lowercase; uppercase variants should not match
    assert get_parser("XML") is None
    assert get_parser("CSV") is None

def test_returns_callable():
    for name in ("xml", "html_tables", "csv", "none"):
        parser = get_parser(name)
        assert callable(parser), f"Expected callable for '{name}', got {parser}"

def test_returns_same_object():
    raw = b"some raw bytes"
    assert return_input(raw) is raw

def test_returns_string_unchanged():
    assert return_input("hello") == "hello"

def test_returns_none_unchanged():
    assert return_input(None) is None

def test_returns_list_unchanged():
    data = [1, 2, 3]
    assert return_input(data) is data


if __name__ == '__main__':
    pytest.main([__file__])

