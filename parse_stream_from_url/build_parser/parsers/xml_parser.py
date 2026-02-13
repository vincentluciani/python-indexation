from lxml import etree
import xml.etree.ElementTree as ET


def parse_xml(raw_stream, parent_tag, child_tag):
    NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    context = etree.iterparse(raw_stream, events=("end",), tag=f"{{{NS['ns']}}}{parent_tag}")
        
    for _, elem in context:
        child = elem.find(f"ns:{child_tag}", NS)
        if child is not None and child.text:
            yield child.text.strip()
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
