"""Parse CSV streams into rows."""

import csv


def parse_csv(stream, parsing_args):
    """Yield CSV rows parsed from a byte stream."""
    separator = parsing_args.get("separator", ",")
    reader = csv.reader(
        (line.decode("utf-8") for line in stream), delimiter=separator
    )
    results = []
    for row in reader:
        results.append(row)
    yield results
