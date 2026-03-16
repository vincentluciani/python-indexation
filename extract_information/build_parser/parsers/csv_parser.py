import csv

def parse_csv(stream, parsing_args):
    # Get separator from parsing_args, default to comma
    separator = parsing_args.get('separator', ',')
    
    reader = csv.reader((line.decode('utf-8') for line in stream), delimiter=separator)
    results = []
    for row in reader:
        results.append(row)
    yield results