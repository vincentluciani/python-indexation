from lxml import html

def parse_html_tables(stream,parsing_args):

    tree = html.parse(stream)
    root = tree.getroot()

    results = []

    # Find all title elements
    for title_tag in root.xpath(f"//{parsing_args.get('title_tag')}"):
        category = title_tag.text_content().strip()

        # Find first table after this element
        table = title_tag.xpath("following-sibling::table[1]")

        if not table:
            continue

        table = table[0]

        rows = table.xpath(".//tr")

        for row in rows:
            cols = row.xpath("./td")
            column_values = []
    
            for col in cols:
                # Find all <br> tags within the cell and replace them with a newline
                for br in col.xpath(".//br"):
                    br.tail = "\n" + (br.tail or "")
                    
                # Extract text; text_content() will now include the newlines we added
                column_values.append(col.text_content().strip())

            results.append({
                "table_title": category,
                "columns_values": column_values
            })

    yield results

