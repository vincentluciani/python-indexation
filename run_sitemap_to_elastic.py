from unicodedata import category
from extract_information.build_decompressor.build_decompressor import get_decompressor
from extract_information.build_parser.build_parser import get_parser
from extract_information.parse_stream_from_url import parse_stream_from_url
from send_information.data_senders.send_data_to_elastic import send_list_of_documents_to_elastic
from extract_information.parse_stream_from_file import parse_stream_from_file
from transform_information.transform_with_ai import summarize_with_ai


if __name__ == "__main__":
    
    url = "https://www.vincent-luciani.com/sitemap.xml.gz"
    parsing_args = {
        "parent_tag": "url",
        "child_tag": "loc"
    }
    
    for url_to_parse in parse_stream_from_url(url,"gzip","xml",parsing_args):
        print("======")
        resulting_learning_table = []
        if "tutorial" in url_to_parse:
            print("Found tutorial URL:", url_to_parse)
            parsing_args = {
                "title_tag":"h2"
            }
            for item in parse_stream_from_url(url_to_parse,"none","html_tables",parsing_args):
                transformed_item = [
                {
                    'category': url_to_parse.split("/")[3], 
                    'sub_category': x.get('table_title', 'N/A'), 
                    'question': x.get('columns_values', ['N/A'])[0] if len(x.get('columns_values', [])) > 1 else 'N/A', 
                    'answer': x.get('columns_values', ['N/A'])[1] if len(x.get('columns_values', [])) > 1 else 'N/A'
                } for x in item]
                resulting_learning_table.append(transformed_item)

            number_of_rows = sum(len(item) for item in resulting_learning_table)
            print(f"url: {url_to_parse}")
            print(f"Total number of rows in the resulting learning table: {number_of_rows}")
            send_list_of_documents_to_elastic(resulting_learning_table[0], "vince")



    


