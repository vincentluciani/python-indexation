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
            results.append({
                "title": category,
                "columns_values": [cols[i].text_content().strip() for i in range(len(cols))]
            })

    yield results

