"""Parse XML sitemap streams with configurable tags."""

from lxml import etree


def parse_xml(raw_stream, parsing_args):
    """Yield text values for configured XML child elements."""
    namespace_map = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    context = etree.iterparse(
        raw_stream,
        events=("end",),
        tag=f"{{{namespace_map['ns']}}}{parsing_args.get('parent_tag')}",
    )  # pylint: disable=no-member

    for _, elem in context:
        child = elem.find(
            f".//ns:{parsing_args.get('child_tag')}", namespace_map
        )
        if child is not None and child.text and child.text.strip():
            yield child.text.strip()
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
