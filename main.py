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
    
    for item in parse_stream_from_url(url,decompressor,parser,parsing_args):
        print("======")
        print(item)
   


    


