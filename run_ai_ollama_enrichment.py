from extract_information.parse_stream_from_file import parse_stream_from_file
from transform_information.transform_with_ai import summarize_with_ai


if __name__ == "__main__":
    
    list_of_suggestions = []
    for parsed_element in parse_stream_from_file("test/test_files/csv_input.csv", 'none', 'csv', {}):
        print(parsed_element)
        list_of_suggestions.extend(parsed_element) # Assuming the suggestions are in the first column of the CSV


    list_of_suggestions = [item[1] for item in list_of_suggestions if item] 
    model = "phi3:mini"
    map_prompt = (
        "You are a product analyst. Extract unique feature requests from the "
        "following customer suggestions. Group similar ideas into one bullet. Be concise."
    )
    list_prefix = "Customer Suggestions"

    reduce_prompt = (
        "You are a lead strategist. Merge the following lists of feature requests "
        "into one master list. Remove any duplicates and combine similar points."
    )
    print("calling summarize_with_ai...")
    test = summarize_with_ai(model, list_of_suggestions, map_prompt, list_prefix)
    print(f"Success! Result length: {len(test)}")
    print("======")
    print(test)

   


    


