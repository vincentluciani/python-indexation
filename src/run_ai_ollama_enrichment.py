"""Run CSV-based AI enrichment using local Ollama."""

from src.extract_information.parse_stream_from_file import parse_stream_from_file
from src.transform_information.transform_with_ai import summarize_with_ai


def main():
    """Run CSV-based AI enrichment using local Ollama."""
    list_of_suggestions = []
    for parsed_element in parse_stream_from_file(
        {
            "file_path": "test/test_files/csv_input.csv",
            "decompressor": "none",
            "parser": "csv",
        }
    ):
        print(parsed_element)
        list_of_suggestions.extend(parsed_element)

    list_of_suggestions = [item[1] for item in list_of_suggestions if item]
    model_name = "phi3:mini"
    map_prompt = (
        "You are a product analyst. Extract unique feature requests from "
        "the following customer suggestions. Group similar ideas into one "
        "bullet. Be concise."
    )
    list_prefix = "Customer Suggestions"
    print("calling summarize_with_ai...")
    result = summarize_with_ai(
        model_name,
        list_of_suggestions,
        map_prompt,
        list_prefix,
    )
    print(f"Success! Result length: {len(result)}")
    print("======")
    print(result)


if __name__ == "__main__":
    main()
