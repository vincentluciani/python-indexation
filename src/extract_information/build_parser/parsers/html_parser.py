"""Parse HTML tables with titles into structured values."""

from lxml import html


def parse_html_tables_with_titles(stream, parsing_args):
    """Parse HTML tables with title associations."""
    tree = html.parse(stream)
    root = tree.getroot()

    results = []
    title_tag_name = parsing_args.get("title_tag")

    title_tags = root.xpath(f"//{title_tag_name}")

    for title_tag in title_tags:
        category = title_tag.text_content().strip()
        table = _find_next_table(title_tag, title_tag_name)

        if table is not None:
            _process_table_rows(table, category, results)

    yield results


def _find_next_table(title_tag, title_tag_name):
    """Find the first table after a title element."""
    following_elements = title_tag.xpath("following-sibling::*")
    base_tag = title_tag_name.split("[")[0]

    for element in following_elements:
        if element.tag == base_tag:
            break
        if element.tag == "table":
            return element
    return None


def _process_table_rows(table, category, results):
    """Process all rows in a table."""
    rows = table.xpath(".//tr")

    if not rows:
        return

    for row in rows:
        cols = row.xpath("./th") + row.xpath("./td")
        if cols:
            column_values = _extract_cell_data(cols)
            results.append(
                {
                    "table_title": category,
                    "columns_values": column_values,
                }
            )


def _extract_cell_data(cells):
    """Extract and clean data from table cells."""
    return [_clean_cell(cell) for cell in cells]


def _clean_cell(cell):
    """Clean a table cell and normalize its text content."""
    _replace_br_with_newlines(cell)
    return _normalize_cell_text(cell.text_content())


def _replace_br_with_newlines(cell):
    """Convert HTML <br> tags inside a cell into newline characters."""
    for br in cell.xpath(".//br"):
        br.tail = "\n" + (br.tail or "")


def _normalize_cell_text(text_content):
    """Trim and normalize whitespace in extracted text."""
    text_content = text_content.strip()
    lines = [line.strip() for line in text_content.split("\n") if line.strip()]
    return "\n".join(lines)
