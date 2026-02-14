from unicodedata import category
from extract_information.build_decompressor.build_decompressor import get_decompressor
from extract_information.build_parser.build_parser import get_parser
from extract_information.parse_stream_from_url import parse_stream_from_url

if __name__ == "__main__":
    url = "https://www.vincent-luciani.com/sitemap.xml.gz"
    decompressor = get_decompressor('gzip')
    parser = get_parser('xml')
    parsing_args = {
        "parent_tag": "url",
        "child_tag": "loc"
    }
    
    for url_to_parse in parse_stream_from_url(url,decompressor,parser,parsing_args):
        print("======")
        resulting_learning_table = []
        if "tutorial" in url_to_parse:
            print("Found tutorial URL:", url_to_parse)
            decompressor = get_decompressor('none')
            parser = get_parser('html_tables')
            parsing_args = {
                "title_tag":"h2"
            }
            for item in parse_stream_from_url(url_to_parse,decompressor,parser,parsing_args):
                transformed_item = [
                {
                    'category': url_to_parse.split("/")[3], # Assuming the category is the 4th segment of the URL
                    'sub_category': x.get('table_title', 'N/A'), # Using the table title as sub-category
                    'question': x.get('columns_values', ['N/A'])[0] if len(x.get('columns_values', [])) > 1 else 'N/A', # Assuming the first column value is the question
                    'answer': x.get('columns_values', ['N/A'])[1] if len(x.get('columns_values', [])) > 1 else 'N/A'
                } for x in item]
                resulting_learning_table.append(transformed_item)

            number_of_rows = sum(len(item) for item in resulting_learning_table)
            print(f"url: {url_to_parse}")
            print(f"Total number of rows in the resulting learning table: {number_of_rows}")


    


