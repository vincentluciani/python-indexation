"""Parse XML sitemap streams with configurable tags."""

# pylint: disable=c-extension-no-member
from lxml import etree


def parse_xml(raw_stream, parsing_args):
    """Yield text values for configured XML child elements."""
    namespace_map = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    for _, elem in _iter_parse(raw_stream, namespace_map, parsing_args):
        text_value = _extract_child_text(elem, namespace_map, parsing_args)
        if text_value is not None:
            yield text_value
        _clear_element(elem)


def _iter_parse(raw_stream, namespace_map, parsing_args):
    """Return an iterator over parsed XML elements."""
    return etree.iterparse(  # pylint: disable=no-member
        raw_stream,
        events=("end",),
        tag=f"{{{namespace_map['ns']}}}{parsing_args.get('parent_tag')}",
    )


def _extract_child_text(elem, namespace_map, parsing_args):
    """Return stripped text for the configured child tag, if present."""
    child = elem.find(
        f".//ns:{parsing_args.get('child_tag')}",
        namespace_map,
    )
    if child is None or child.text is None:
        return None

    text_value = child.text.strip()
    return text_value if text_value else None


def _clear_element(elem):
    """Remove a parsed XML element from memory after processing."""
    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]
