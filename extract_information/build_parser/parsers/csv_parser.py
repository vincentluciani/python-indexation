import csv

def parse_csv(stream, parsing_args):
    reader = csv.reader((line.decode('utf-8') for line in stream))
    results = []
    for row in reader:
        results.append(row)
    yield results