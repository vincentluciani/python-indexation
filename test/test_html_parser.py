import pytest
from io import BytesIO
from extract_information.build_parser.parsers.html_parser import parse_html_tables


def test_parse_html_tables_basic():
    """Test basic HTML table parsing functionality"""
    html_content = b"""
    <html>
    <body>
        <h2>Category 1</h2>
        <table>
            <tr><td>Cell 1</td><td>Cell 2</td></tr>
            <tr><td>Cell 3</td><td>Cell 4</td></tr>
        </table>
        
        <h2>Category 2</h2>
        <table>
            <tr><td>Cell A</td><td>Cell B</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Category 1",
            "columns_values": ["Cell 1", "Cell 2"]
        },
        {
            "table_title": "Category 1", 
            "columns_values": ["Cell 3", "Cell 4"]
        },
        {
            "table_title": "Category 2",
            "columns_values": ["Cell A", "Cell B"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_with_br_tags():
    """Test parsing HTML tables with <br> tags in cells"""
    html_content = b"""
    <html>
    <body>
        <h2>Test Category</h2>
        <table>
            <tr><td>Line 1<br>Line 2</td><td>Single Line</td></tr>
            <tr><td>No Break</td><td>First<br>Second<br>Third</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Test Category",
            "columns_values": ["Line 1\nLine 2", "Single Line"]
        },
        {
            "table_title": "Test Category",
            "columns_values": ["No Break", "First\nSecond\nThird"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_empty_table():
    """Test parsing HTML with empty table"""
    html_content = b"""
    <html>
    <body>
        <h2>Empty Category</h2>
        <table>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    assert result == [[]]


def test_parse_html_tables_no_table_after_title():
    """Test parsing HTML when title has no following table"""
    html_content = b"""
    <html>
    <body>
        <h2>No Table Category</h2>
        <div>Some content</div>
        <h2>Valid Category</h2>
        <table>
            <tr><td>Valid Cell</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Valid Category",
            "columns_values": ["Valid Cell"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_missing_table_between_titles():
    """Test parsing HTML when there's no table between some titles"""
    html_content = b"""
    <html>
    <body>
        <h2>Title 1</h2>
        <div>No table here</div>
        <h2>Title 2</h2>
        <table>
            <tr><td>Table 2 Cell</td></tr>
        </table>
        <h2>Title 3</h2>
        <div>No table here either</div>
        <h2>Title 4</h2>
        <table>
            <tr><td>Table 4 Cell</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Title 2",
            "columns_values": ["Table 2 Cell"]
        },
        {
            "table_title": "Title 4",
            "columns_values": ["Table 4 Cell"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_title_before_another_title():
    """Test parsing when another title appears before a table"""
    html_content = b"""
    <html>
    <body>
        <h2>Title 1</h2>
        <div>Some content</div>
        <h2>Title 2</h2>
        <table>
            <tr><td>Should be associated with Title 2</td></tr>
        </table>
        <h2>Title 3</h2>
        <p>Paragraph content</p>
        <h2>Title 4</h2>
        <table>
            <tr><td>Should be associated with Title 4</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Title 2",
            "columns_values": ["Should be associated with Title 2"]
        },
        {
            "table_title": "Title 4",
            "columns_values": ["Should be associated with Title 4"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_complex_xpath_titles():
    """Test parsing with complex XPath title selectors"""
    html_content = b"""
    <html>
    <body>
        <h2 class="section">Title 1</h2>
        <div>Content</div>
        <h2 class="section">Title 2</h2>
        <table>
            <tr><td>Table for Title 2</td></tr>
        </table>
        <h3>Different Title</h3>
        <table>
            <tr><td>Should not be associated</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2[@class="section"]'}))
    
    expected = [
        {
            "table_title": "Title 2",
            "columns_values": ["Table for Title 2"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_different_title_tags():
    """Test parsing with different title tag types"""
    html_content = b"""
    <html>
    <body>
        <h1>Title 1</h1>
        <table>
            <tr><td>H1 Cell</td></tr>
        </table>
        <h3>Title 3</h3>
        <table>
            <tr><td>H3 Cell</td></tr>
        </table>
        <div class="title">Div Title</div>
        <table>
            <tr><td>Div Cell</td></tr>
        </table>
    </body>
    </html>
    """
    
    # Test with h1
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h1'}))
    
    expected = [
        {
            "table_title": "Title 1",
            "columns_values": ["H1 Cell"]
        }
    ]
    assert result == [expected]
    
    # Test with h3
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h3'}))
    
    expected = [
        {
            "table_title": "Title 3",
            "columns_values": ["H3 Cell"]
        }
    ]
    assert result == [expected]
    
    # Test with div
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'div[@class="title"]'}))
    
    expected = [
        {
            "table_title": "Div Title",
            "columns_values": ["Div Cell"]
        }
    ]
    assert result == [expected]


def test_parse_html_tables_with_empty_cells():
    """Test parsing tables with empty cells"""
    html_content = b"""
    <html>
    <body>
        <h2>Empty Cells Test</h2>
        <table>
            <tr><td></td><td>Non-empty</td></tr>
            <tr><td>Cell A</td><td></td></tr>
            <tr><td></td><td></td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Empty Cells Test",
            "columns_values": ["", "Non-empty"]
        },
        {
            "table_title": "Empty Cells Test",
            "columns_values": ["Cell A", ""]
        },
        {
            "table_title": "Empty Cells Test",
            "columns_values": ["", ""]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_with_whitespace():
    """Test parsing tables with whitespace in cells"""
    html_content = b"""
    <html>
    <body>
        <h2>Whitespace Test</h2>
        <table>
            <tr><td>  Spaced Text  </td><td>\tTabbed Text\t</td></tr>
            <tr><td>\nNewline Text\n</td><td>   Mixed   </td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Whitespace Test",
            "columns_values": ["Spaced Text", "Tabbed Text"]
        },
        {
            "table_title": "Whitespace Test",
            "columns_values": ["Newline Text", "Mixed"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_nested_elements():
    """Test parsing tables with nested elements in cells"""
    html_content = b"""
    <html>
    <body>
        <h2>Nested Elements</h2>
        <table>
            <tr><td><strong>Bold Text</strong></td><td><em>Italic Text</em></td></tr>
            <tr><td><a href="#">Link Text</a></td><td><span>Span Text</span></td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Nested Elements",
            "columns_values": ["Bold Text", "Italic Text"]
        },
        {
            "table_title": "Nested Elements",
            "columns_values": ["Link Text", "Span Text"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_generator_behavior():
    """Test that parse_html_tables returns a generator"""
    html_content = b"""
    <html>
    <body>
        <h2>Test</h2>
        <table>
            <tr><td>Cell</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    generator = parse_html_tables(stream, {'title_tag': 'h2'})
    
    # Check if it's a generator
    assert hasattr(generator, '__iter__')
    assert hasattr(generator, '__next__')
    
    # Convert to list to get results
    result = list(generator)
    expected = [
        {
            "table_title": "Test",
            "columns_values": ["Cell"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_no_title_tag():
    """Test parsing when no title tag is found"""
    html_content = b"""
    <html>
    <body>
        <table>
            <tr><td>Orphan Cell</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    assert result == [[]]


def test_parse_html_tables_mixed_content():
    """Test parsing with mixed HTML content"""
    html_content = b"""
    <html>
    <body>
        <h2>Mixed Content</h2>
        <p>Some paragraph text</p>
        <table>
            <tr><td>Cell 1<br>with break</td><td>Normal Cell</td></tr>
        </table>
        <div>More content</div>
        <table>
            <tr><td>Second table</td></tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Mixed Content",
            "columns_values": ["Cell 1\nwith break", "Normal Cell"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_with_styled_cells():
    """Test parsing tables with styled cells"""
    html_content = b"""
    <html>
    <body>
        <h2>Styled Table</h2>
        <table>
            <tr>
                <td style="color: red; font-weight: bold;">Red Bold Text</td>
                <td class="highlight">Highlighted Cell</td>
                <td><span style="background: yellow;">Yellow Background</span></td>
            </tr>
            <tr>
                <td><div class="content">Div Content</div></td>
                <td><em>Italic Text</em></td>
                <td><strong>Strong Text</strong></td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Styled Table",
            "columns_values": ["Red Bold Text", "Highlighted Cell", "Yellow Background"]
        },
        {
            "table_title": "Styled Table",
            "columns_values": ["Div Content", "Italic Text", "Strong Text"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_with_header_tags():
    """Test parsing tables with special header tags (th, thead)"""
    html_content = b"""
    <html>
    <body>
        <h2>Table with Headers</h2>
        <table>
            <thead>
                <tr>
                    <th>Header 1</th>
                    <th>Header 2</th>
                    <th>Header 3</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Data 1</td>
                    <td>Data 2</td>
                    <td>Data 3</td>
                </tr>
                <tr>
                    <td>More 1</td>
                    <td>More 2</td>
                    <td>More 3</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Table with Headers",
            "columns_values": ["Header 1", "Header 2", "Header 3"]
        },
        {
            "table_title": "Table with Headers",
            "columns_values": ["Data 1", "Data 2", "Data 3"]
        },
        {
            "table_title": "Table with Headers",
            "columns_values": ["More 1", "More 2", "More 3"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_mixed_headers_and_data():
    """Test parsing tables with mixed th and td tags"""
    html_content = b"""
    <html>
    <body>
        <h2>Mixed Headers</h2>
        <table>
            <tr>
                <th>Name</th>
                <td>John</td>
                <td>Age</td>
            </tr>
            <tr>
                <th>City</th>
                <td>New York</td>
                <td>Country</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Mixed Headers",
            "columns_values": ["Name", "John", "Age"]
        },
        {
            "table_title": "Mixed Headers",
            "columns_values": ["City", "New York", "Country"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_complex_styling():
    """Test parsing tables with complex styling and nested elements"""
    html_content = b"""
    <html>
    <body>
        <h2>Complex Styling</h2>
        <table>
            <tr>
                <td style="padding: 10px; border: 1px solid #ccc;">
                    <div class="cell-content">
                        <span style="color: #333;">Styled Text</span>
                        <br>
                        <small>Small text</small>
                    </div>
                </td>
                <td bgcolor="#f0f0f0">
                    <a href="#">Link Text</a>
                    <br>
                    <em>Emphasized</em>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Complex Styling",
            "columns_values": ["Styled Text\nSmall text", "Link Text\nEmphasized"]
        }
    ]
    
    assert result == [expected]


def test_parse_html_tables_empty_headers():
    """Test parsing tables with empty header cells"""
    html_content = b"""
    <html>
    <body>
        <h2>Empty Headers</h2>
        <table>
            <tr>
                <th></th>
                <th>Header 2</th>
                <th></th>
            </tr>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
                <td>Data 3</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    stream = BytesIO(html_content)
    result = list(parse_html_tables(stream, {'title_tag': 'h2'}))
    
    expected = [
        {
            "table_title": "Empty Headers",
            "columns_values": ["", "Header 2", ""]
        },
        {
            "table_title": "Empty Headers",
            "columns_values": ["Data 1", "Data 2", "Data 3"]
        }
    ]
    
    assert result == [expected]


if __name__ == '__main__':
    pytest.main([__file__])
