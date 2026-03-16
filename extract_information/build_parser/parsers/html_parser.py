from lxml import html

def parse_html_tables(stream,parsing_args):

    tree = html.parse(stream)
    root = tree.getroot()

    results = []
    title_tag_name = parsing_args.get('title_tag')

    # Find all title elements
    for title_tag in root.xpath(f"//{title_tag_name}"):
        category = title_tag.text_content().strip()

        # Find first table after this title, but stop if we encounter another title
        following_elements = title_tag.xpath("following-sibling::*")
        table = None
        
        for element in following_elements:
            # If we encounter another title, stop looking
            # Extract the base tag name (without attributes) for comparison
            base_tag = title_tag_name.split('[')[0]
            if element.tag == base_tag:
                break
            # If we find a table, use it and stop looking
            if element.tag == 'table':
                table = element
                break

        if table is None:
            continue

        rows = table.xpath(".//tr")

        for row in rows:
            cols = row.xpath("./td")
            column_values = []
    
            for col in cols:
                # Find all <br> tags within the cell and replace them with a newline
                for br in col.xpath(".//br"):
                    br.tail = "\n" + (br.tail or "")
                    
                # Extract text; text_content() will now include the newlines we added
                # Clean up whitespace: replace multiple spaces/newlines with single spaces/newlines
                text_content = col.text_content().strip()
                # Replace multiple newlines with single newline and clean up spacing
                lines = [line.strip() for line in text_content.split('\n') if line.strip()]
                cleaned_text = '\n'.join(lines)
                
                column_values.append(cleaned_text)

            results.append({
                "table_title": category,
                "columns_values": column_values
            })

    yield results

