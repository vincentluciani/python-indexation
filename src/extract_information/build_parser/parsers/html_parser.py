from lxml import html

def parse_html_tables_with_titles(stream, parsing_args):
    """Parse HTML tables with title associations"""
    tree = html.parse(stream)
    root = tree.getroot()
    
    results = []
    title_tag_name = parsing_args.get('title_tag')
    
    # Process tables with titles
    title_tags = root.xpath(f"//{title_tag_name}")
    
    for title_tag in title_tags:
        category = title_tag.text_content().strip()
        table = _find_next_table(title_tag, title_tag_name)
        
        if table is not None:
            _process_table_rows(table, category, results)
  
    yield results


def _find_next_table(title_tag, title_tag_name):
    """Find the first table after a title element"""
    following_elements = title_tag.xpath("following-sibling::*")
    base_tag = title_tag_name.split('[')[0]
    
    for element in following_elements:
        if element.tag == base_tag:
            break  # Stop at another title
        if element.tag == 'table':
            return element
    return None

def _process_table_rows(table, category, results):
    """Process all rows in a table"""
    rows = table.xpath(".//tr")
    
    if not rows:
        return
    
    for row in rows:
        cols = row.xpath("./th") + row.xpath("./td")
        if cols:
            column_values = _extract_cell_data(cols)
            results.append({
                "table_title": category,
                "columns_values": column_values
            })


def _extract_cell_data(cells):
    """Extract and clean data from table cells"""
    column_values = []
    
    for cell in cells:
        # Find all <br> tags within cell and replace them with a newline
        for br in cell.xpath(".//br"):
            br.tail = "\n" + (br.tail or "")
        
        # Extract text and clean whitespace
        text_content = cell.text_content().strip()
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        column_values.append(cleaned_text)
    
    return column_values
