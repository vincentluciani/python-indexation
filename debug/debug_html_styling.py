from io import BytesIO
from src.extract_information.build_parser.parsers.html_parser import parse_html_tables

# Test the complex styling case
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

print("=== Debug Complex Styling Test ===")
print(f"Actual result: {result}")

expected = [
    {
        "table_title": "Complex Styling",
        "columns_values": ["Styled Text\nSmall text", "Link Text\nEmphasized"]
    }
]

print(f"Expected result: {expected}")
print(f"Match: {result == [expected]}")

if result != [expected]:
    print("Differences:")
    for i, (actual, exp) in enumerate(zip(result[0], expected)):
        if actual != exp:
            print(f"  Row {i}:")
            print(f"    Actual: {actual}")
            print(f"    Expected: {exp}")
