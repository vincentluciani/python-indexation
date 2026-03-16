from lxml import html

def parse_html_tables_with_titles(stream, parsing_args):
    """Parse HTML tables with title associations"""
    tree = html.parse(stream)
    root = tree.getroot()
    
    results = []
    title_tag_name = parsing_args.get('title_tag')
    
    # Process tables with titles
    title_tags = root.xpath(f"//{title_tag_name}")
    
    for i, title_tag in enumerate(title_tags):
        category = title_tag.text_content().strip()
        table = _find_next_table(title_tag, title_tag_name)
        
        if table:
            _process_table_rows(table, category, results)
        else:
            # If no table found for this title, check if next title should take over
            if i + 1 < len(title_tags):
                # Let next title try to find a table
                pass  # Next iteration will handle it
            else:
                # Last title with no table - nothing to do
                pass
    
    # Process orphaned tables (tables without preceding titles)
    _process_orphaned_tables(root, title_tag_name, results)
    
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


def _process_orphaned_tables(root, title_tag_name, results):
    """Process tables that don't have preceding titles"""
    all_tables = root.xpath("//table")
    processed_tables = set()
    
    # Mark tables already processed with titles
    for title_tag in root.xpath(f"//{title_tag_name}"):
        table = _find_next_table(title_tag, title_tag_name)
        if table:
            processed_tables.add(id(table))
    
    # Process remaining tables
    for table in all_tables:
        if id(table) not in processed_tables:
            if not _has_preceding_title(table, title_tag_name):
                _process_table_rows(table, "", results)


def _has_preceding_title(table, title_tag_name):
    """Check if table has a preceding title element"""
    preceding_elements = table.xpath("preceding-sibling::*")
    base_tag = title_tag_name.split('[')[0]
    
    for element in preceding_elements:
        if element.tag == base_tag:
            return True
    return False


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
