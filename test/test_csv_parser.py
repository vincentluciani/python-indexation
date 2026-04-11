import pytest
import csv
from src.extract_information.build_parser.parsers.csv_parser import parse_csv


def test_parse_csv_basic():
    """Test basic CSV parsing functionality"""
    # Create mock stream with CSV data
    csv_data = [
        b'name,age,city\n',
        b'John,25,New York\n',
        b'Jane,30,Los Angeles\n',
        b'Bob,35,Chicago\n'
    ]
    
    # Test the parser
    result = list(parse_csv(iter(csv_data), {}))
    
    # Expected result
    expected = [['name', 'age', 'city'], 
                ['John', '25', 'New York'], 
                ['Jane', '30', 'Los Angeles'], 
                ['Bob', '35', 'Chicago']]
    
    assert result == [expected]

def test_parse_csv_empty_fields():
    """Test parsing empty CSV data"""
    csv_data = [
        b'name,age,city\n',
        b',25,\n',
        b',,\n',
        b'Bob,35,Chicago\n'
    ]
    
    result = list(parse_csv(iter(csv_data), {}))
    
    # Expected result
    expected = [['name', 'age', 'city'], 
                ['', '25', ''], 
                ['', '', ''], 
                ['Bob', '35', 'Chicago']]

    assert result == [expected]

def test_parse_csv_empty_lines():
    """Test parsing empty CSV data"""
    csv_data = [
        b'name,age,city\n',
        b'\n',
        b'Bob,35,Chicago\n',
        b'\n',
        b'Joe,65,New-York\n'
    ]
    
    result = list(parse_csv(iter(csv_data), {}))
    
    # Expected result
    expected = [['name', 'age', 'city'], 
                [],  
                ['Bob', '35', 'Chicago'],
                [],
                ['Joe', '65', 'New-York']]

    assert result == [expected]

def test_parse_csv_basic():
    """Test basic CSV parsing functionality"""
    # Create mock stream with CSV data
    csv_data = [
        b'name,age,city\n',
        b'John,25,New York\n',
        b'Jane,30,Los Angeles\n',
        b'Bob,35,Chicago\n'
    ]
    
    # Test the parser
    result = list(parse_csv(iter(csv_data), {}))
    
    # Expected result
    expected = [['name', 'age', 'city'], 
                ['John', '25', 'New York'], 
                ['Jane', '30', 'Los Angeles'], 
                ['Bob', '35', 'Chicago']]
    
    assert result == [expected]

def test_parse_csv_single_row():
    """Test parsing CSV with single row"""
    csv_data = [b'header1,header2,header3\n']
    
    result = list(parse_csv(iter(csv_data), {}))
    
    expected = [['header1', 'header2', 'header3']]
    assert result == [expected]

def test_parse_csv_with_quotes():
    """Test parsing CSV with quoted fields"""
    csv_data = [
        b'name,description\n',
        b'John,"A person with, comma"\n',
        b'Jane,"Normal description"\n'
    ]
    
    result = list(parse_csv(iter(csv_data), {}))
    
    expected = [
        ['name', 'description'],
        ['John', 'A person with, comma'],
        ['Jane', 'Normal description']
    ]
    assert result == [expected]

def test_parse_csv_with_empty_fields():
    """Test parsing CSV with empty fields"""
    csv_data = [
        b'name,age,city\n',
        b'John,,New York\n',
        b',30,\n'
    ]
    
    result = list(parse_csv(iter(csv_data), {}))
    
    expected = [
        ['name', 'age', 'city'],
        ['John', '', 'New York'],
        ['', '30', '']
    ]
    assert result == [expected]

def test_parse_csv_unicode_characters():
    """Test parsing CSV with Unicode characters"""
    csv_data = [
        'name,city\n',
        'José,São Paulo\n',
        'François,Paris\n'
    ]
    
    # Convert strings to UTF-8 bytes as the parser expects
    csv_data_bytes = [line.encode('utf-8') for line in csv_data]
    
    result = list(parse_csv(iter(csv_data_bytes), {}))
    
    expected = [
        ['name', 'city'],
        ['José', 'São Paulo'],
        ['François', 'Paris']
    ]
    assert result == [expected]

def test_parse_csv_multilingual_characters():
    """Test parsing CSV with Chinese, Hindi, and Korean characters"""
    csv_data = [
        'name,city,country\n',
        '张伟,北京,中国\n',
        'राज,मुंबई,भारत\n',
        '김철수,서울,한국\n'
    ]
    
    # Convert strings to UTF-8 bytes as the parser expects
    csv_data_bytes = [line.encode('utf-8') for line in csv_data]
    
    result = list(parse_csv(iter(csv_data_bytes), {}))
    
    expected = [
        ['name', 'city', 'country'],
        ['张伟', '北京', '中国'],
        ['राज', 'मुंबई', 'भारत'],
        ['김철수', '서울', '한국']
    ]
    assert result == [expected]

def test_parse_csv_uneven_fields():
    """Test parsing CSV with uneven number of fields between lines"""
    csv_data = [
        b'name,age,city,country\n',
        b'John,25,New York,USA\n',
        b'Jane,30,Los Angeles\n',  # Missing country field
        b'Bob,35,Chicago,USA,Extra\n',  # Extra field
        b'Alice,28\n'  # Missing city and country fields
    ]
    
    result = list(parse_csv(iter(csv_data), {}))
    
    expected = [
        ['name', 'age', 'city', 'country'],
        ['John', '25', 'New York', 'USA'],
        ['Jane', '30', 'Los Angeles'],  # Shorter row
        ['Bob', '35', 'Chicago', 'USA', 'Extra'],  # Longer row
        ['Alice', '28']  # Even shorter row
    ]
    assert result == [expected]

def test_parse_csv_default_separator():
    """Test parsing CSV with default comma separator when no separator specified"""
    csv_data = [
        b'name,age,city\n',
        b'John,25,New York\n',
        b'Jane,30,Los Angeles\n'
    ]
    
    # Test with empty parsing_args (should default to comma)
    result = list(parse_csv(iter(csv_data), {}))
    
    expected = [
        ['name', 'age', 'city'],
        ['John', '25', 'New York'],
        ['Jane', '30', 'Los Angeles']
    ]
    assert result == [expected]
    
    # Test with explicit comma separator
    result = list(parse_csv(iter(csv_data), {'separator': ','}))
    
    assert result == [expected]

def test_parse_csv_semicolon_separator():
    """Test parsing CSV with semicolon separator"""
    csv_data = [
        b'name;age;city\n',
        b'John;25;New York\n',
        b'Jane;30;Los Angeles\n'
    ]
    
    result = list(parse_csv(iter(csv_data), {'separator': ';'}))
    
    expected = [
        ['name', 'age', 'city'],
        ['John', '25', 'New York'],
        ['Jane', '30', 'Los Angeles']
    ]
    assert result == [expected]

def test_parse_csv_tab_separator():
    """Test parsing CSV with tab separator"""
    csv_data = [
        b'name\tage\tcity\n',
        b'John\t25\tNew York\n',
        b'Jane\t30\tLos Angeles\n'
    ]
    
    result = list(parse_csv(iter(csv_data), {'separator': '\t'}))
    
    expected = [
        ['name', 'age', 'city'],
        ['John', '25', 'New York'],
        ['Jane', '30', 'Los Angeles']
    ]
    assert result == [expected]

def test_parse_csv_pipe_separator():
    """Test parsing CSV with pipe separator"""
    csv_data = [
        b'name|age|city\n',
        b'John|25|New York\n',
        b'Jane|30|Los Angeles\n'
    ]
    
    result = list(parse_csv(iter(csv_data), {'separator': '|'}))
    
    expected = [
        ['name', 'age', 'city'],
        ['John', '25', 'New York'],
        ['Jane', '30', 'Los Angeles']
    ]
    assert result == [expected]

def test_parse_csv_newline_in_quoted_field():
    """Test parsing CSV with newline in quoted field"""
    csv_data = [
        b'name,description\n',
        b'John,"A person with\nnewline in description"\n',
        b'Jane,"Normal description"\n'
    ]
    
    result = list(parse_csv(iter(csv_data), {}))
    
    expected = [
        ['name', 'description'],
        ['John', 'A person with\nnewline in description'],
        ['Jane', 'Normal description']
    ]
    assert result == [expected]

def test_parse_csv_newline_in_unquoted_field():
    """Test parsing CSV with newline in unquoted field (should raise error)"""
    csv_data = [
        b'name,description\n',
        b'John,A person with\nnewline in unquoted field\n',
        b'Jane,Normal description\n'
    ]
    
    # CSV parser should raise an error for newlines in unquoted fields
    with pytest.raises(csv.Error, match="new-line character seen in unquoted field"):
        list(parse_csv(iter(csv_data), {}))

def test_parse_csv_generator_behavior():
    """Test that parse_csv returns a generator"""
    csv_data = [b'test,data\n']
    
    generator = parse_csv(iter(csv_data), {})
    
    # Check if it's a generator
    assert hasattr(generator, '__iter__')
    assert hasattr(generator, '__next__')
    
    # Convert to list to get results
    result = list(generator)
    # The parser yields a list containing the parsed rows, 
    # and list() wraps that in another list
    assert result == [[['test', 'data']]]

def test_parse_csv_big_lines():
    """Test parsing CSV with newline in quoted field"""
    csv_data = []
    expected = [['0_1'], ['1_1']]
    csv_data.append('0_1,'.encode('utf-8'))
    csv_data.append('1_1,'.encode('utf-8'))

    for i in range(2,100):
        csv_data[0] += f'0_{i},'.encode('utf-8')
        csv_data[1] += f'1_{i},'.encode('utf-8')
        expected[0].append(f'0_{i}')
        expected[1].append(f'1_{i}')

    csv_data[0] += '0_100'.encode('utf-8')
    csv_data[1] += '1_100'.encode('utf-8')
    expected[0].append('0_100')
    expected[1].append('1_100')

    result = list(parse_csv(iter(csv_data), {}))
    
    assert result == [expected]

if __name__ == '__main__':
    pytest.main([__file__])
