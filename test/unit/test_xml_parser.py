import pytest
from io import BytesIO
from src.extract_information.build_parser.parsers import xml_parser

def test_parse_xml():
        # In-memory XML stream
        xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://www.example.com/foo.html</loc>
    <lastmod>2022-01-01</lastmod>
  </url>
  <url>
    <loc>http://www.example.com/bar.html</loc>
    <lastmod>2022-02-02</lastmod>
  </url>
</urlset>
""")
        parsing_args = {
            'parent_tag': 'url',
            'child_tag': 'loc'
        }
        expected_output = [
            'http://www.example.com/foo.html',
            'http://www.example.com/bar.html'
        ]
        result = list(xml_parser.parse_xml(xml_stream, parsing_args))
        assert result == expected_output

def test_missing_child_tags():
        # In-memory XML stream
        xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://www.example.com/foo.html</loc>
  </url>
  <url>
  </url>
  <test>test</test>
  <loc>http://www.example.com/foo2.html</loc>
</urlset>
""")

        parsing_args = {
            'parent_tag': 'url',
            'child_tag': 'loc'
        }
        expected_output = ['http://www.example.com/foo.html']
        result = list(xml_parser.parse_xml(xml_stream, parsing_args))
        assert result == expected_output

def test_no_child_tags():
        # In-memory XML stream
        xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
  </url>
  <test>test</test>
  <loc>http://www.example.com/foo2.html</loc>
</urlset>
""")

        # Set up parsing arguments
        parsing_args = {
            'parent_tag': 'url',
            'child_tag': 'loc'
        }

        expected_output = []
        result = list(xml_parser.parse_xml(xml_stream, parsing_args))
        assert result == expected_output

def test_empty_child_tags():
        # In-memory XML stream
        xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>   </loc></url>
</urlset>
""")
        parsing_args = {
            'parent_tag': 'url',
            'child_tag': 'loc'
        }
        expected_output = []
        result = list(xml_parser.parse_xml(xml_stream, parsing_args))
        assert result == expected_output

def test_deeper_level_of_nesting():
        # In-memory XML stream
        xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <sub_url>
            <loc>http://www.example.com/foo.html</loc>
        </sub_url>
    </url>
    <url>
        <sub_url>
            <loc>http://www.example.com/bar.html</loc>
        </sub_url>
    </url>
</urlset>
""")

        parsing_args = {
            'parent_tag': 'url',
            'child_tag': 'loc'
        }
        expected_output = [
            'http://www.example.com/foo.html',
            'http://www.example.com/bar.html'
        ]
        result = list(xml_parser.parse_xml(xml_stream, parsing_args))
        assert result == expected_output

def test_no_namespace():
        # In-memory XML stream
        xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset>
  <url><loc>   </loc></url>
</urlset>
""")

        parsing_args = {
            'parent_tag': 'url',
            'child_tag': 'loc'
        }
        expected_output = []
        result = list(xml_parser.parse_xml(xml_stream, parsing_args))
        assert result == expected_output


def test_no_namespace_with_data():
        # In-memory XML stream
        xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset>
  <url>
    <loc>http://www.example.com/foo.html</loc>
  </url>
</urlset>
""")

        parsing_args = {
            'parent_tag': 'url',
            'child_tag': 'loc'
        }
        expected_output = []
        result = list(xml_parser.parse_xml(xml_stream, parsing_args))
        assert result == expected_output

def test_other_tags():
        # In-memory XML stream
        xml_stream = BytesIO(b"""
<root xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <item><name>test1</name></item>
</root>
""")

        parsing_args = {
            'parent_tag': 'item',
            'child_tag': 'name'
        }
        expected_output = ['test1']
        result = list(xml_parser.parse_xml(xml_stream, parsing_args))
        assert result == expected_output

def test_malformed_xml():
        xml_stream = BytesIO(b"<urlset><url></urlset>")
        parsing_args = {
            'parent_tag': 'url',
            'child_tag': 'loc'
        }
        with pytest.raises(Exception):
            list(xml_parser.parse_xml(xml_stream, parsing_args))


def test_whitespace_stripped_from_content():
    xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>  http://www.example.com/foo.html  </loc></url>
</urlset>
""")
    parsing_args = {'parent_tag': 'url', 'child_tag': 'loc'}
    result = list(xml_parser.parse_xml(xml_stream, parsing_args))
    assert result == ['http://www.example.com/foo.html']


def test_multiple_child_tags_under_same_parent():
    # find() returns the first match only
    xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://www.example.com/first.html</loc>
    <loc>http://www.example.com/second.html</loc>
  </url>
</urlset>
""")
    parsing_args = {'parent_tag': 'url', 'child_tag': 'loc'}
    result = list(xml_parser.parse_xml(xml_stream, parsing_args))
    assert result == ['http://www.example.com/first.html']


def test_unicode_content():
    xml_stream = BytesIO("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>http://www.example.com/\u4e2d\u6587.html</loc></url>
  <url><loc>http://www.example.com/caf\xe9.html</loc></url>
</urlset>
""".encode("utf-8"))
    parsing_args = {'parent_tag': 'url', 'child_tag': 'loc'}
    result = list(xml_parser.parse_xml(xml_stream, parsing_args))
    assert result == [
        'http://www.example.com/\u4e2d\u6587.html',
        'http://www.example.com/caf\xe9.html',
    ]


def test_empty_root_no_parent_elements():
    xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</urlset>
""")
    parsing_args = {'parent_tag': 'url', 'child_tag': 'loc'}
    result = list(xml_parser.parse_xml(xml_stream, parsing_args))
    assert result == []


def test_large_document():
    n = 1000
    urls = b"\n".join(
        f"  <url><loc>http://www.example.com/page{i}.html</loc></url>".encode()
        for i in range(n)
    )
    xml_stream = BytesIO(
        b'<?xml version="1.0" encoding="UTF-8"?>\n'
        b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls +
        b'\n</urlset>'
    )
    parsing_args = {'parent_tag': 'url', 'child_tag': 'loc'}
    result = list(xml_parser.parse_xml(xml_stream, parsing_args))
    assert len(result) == n
    assert result[0] == 'http://www.example.com/page0.html'
    assert result[-1] == f'http://www.example.com/page{n - 1}.html'


def test_missing_parent_tag_key_returns_empty():
    # parsing_args.get() returns None → tag pattern won't match anything
    xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>http://www.example.com/foo.html</loc></url>
</urlset>
""")
    parsing_args = {'child_tag': 'loc'}  # parent_tag intentionally omitted
    result = list(xml_parser.parse_xml(xml_stream, parsing_args))
    assert result == []


def test_child_tag_not_under_parent():
    # loc exists in the document but not as a descendant of url
    xml_stream = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><lastmod>2024-01-01</lastmod></url>
  <loc>http://www.example.com/foo.html</loc>
</urlset>
""")
    parsing_args = {'parent_tag': 'url', 'child_tag': 'loc'}
    result = list(xml_parser.parse_xml(xml_stream, parsing_args))
    assert result == []


if __name__ == '__main__':
    pytest.main([__file__])
