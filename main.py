from unicodedata import category
from extract_information.build_decompressor.build_decompressor import get_decompressor
from extract_information.build_parser.build_parser import get_parser
from extract_information.parse_stream_from_url import parse_stream_from_url
from send_information.data_senders.send_data_to_elastic import send_list_of_documents_to_elastic
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

    # url = "https://www.vincent-luciani.com/sitemap.xml.gz"
    # parsing_args = {
    #     "parent_tag": "url",
    #     "child_tag": "loc"
    # }
    
    # for url_to_parse in parse_stream_from_url(url,"gzip","xml",parsing_args):
    #     print("======")
    #     resulting_learning_table = []
    #     if "tutorial" in url_to_parse:
    #         print("Found tutorial URL:", url_to_parse)
    #         parsing_args = {
    #             "title_tag":"h2"
    #         }
    #         for item in parse_stream_from_url(url_to_parse,"none","html_tables",parsing_args):
    #             transformed_item = [
    #             {
    #                 'category': url_to_parse.split("/")[3], # Assuming the category is the 4th segment of the URL
    #                 'sub_category': x.get('table_title', 'N/A'), # Using the table title as sub-category
    #                 'question': x.get('columns_values', ['N/A'])[0] if len(x.get('columns_values', [])) > 1 else 'N/A', # Assuming the first column value is the question
    #                 'answer': x.get('columns_values', ['N/A'])[1] if len(x.get('columns_values', [])) > 1 else 'N/A'
    #             } for x in item]
    #             resulting_learning_table.append(transformed_item)

    #         number_of_rows = sum(len(item) for item in resulting_learning_table)
    #         print(f"url: {url_to_parse}")
    #         print(f"Total number of rows in the resulting learning table: {number_of_rows}")
    #         send_list_of_documents_to_elastic(resulting_learning_table[0], "vince")



    


