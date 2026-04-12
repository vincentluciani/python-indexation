from src.extract_information.build_parser.parsers.csv_parser import parse_csv

# Debug the CSV parser
csv_data = [b'test,data\n']

print("=== Debug CSV Parser ===")
print(f"Input data: {csv_data}")

# Get the generator
generator = parse_csv(iter(csv_data), {})
print(f"Generator type: {type(generator)}")

# Get the first yielded value
first_yield = next(generator)
print(f"First yielded value: {first_yield}")
print(f"First yielded value type: {type(first_yield)}")
print(f"First yielded value length: {len(first_yield)}")

# Convert to list
generator = parse_csv(iter(csv_data), {})
result = list(generator)
print(f"Full result: {result}")
print(f"Result type: {type(result)}")
print(f"Result length: {len(result)}")

if len(result) > 0:
    print(f"result[0]: {result[0]}")
    print(f"result[0] type: {type(result[0])}")
    print(f"result[0] length: {len(result[0])}")
