from src.extract_information.build_parser.parsers.csv_parser import parse_csv

# Debug newline in unquoted field
csv_data = [
    b'name,description\n',
    b'John,A person with\nnewline in unquoted field\n',
    b'Jane,Normal description\n'
]

print("=== Debug Newline in Unquoted Field ===")
print(f"Input data: {csv_data}")

result = list(parse_csv(iter(csv_data), {}))
print(f"Actual result: {result}")
print(f"Result length: {len(result[0])}")
for i, row in enumerate(result[0]):
    print(f"Row {i}: {row}")
