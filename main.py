from parse_stream_from_url.parse_xml_from_url import parse_xml_stream_from_url

if __name__ == "__main__":
    url = "https://www.vincent-luciani.com/sitemap.xml.gz"

    for item in parse_xml_stream_from_url(url,"url","loc"):
        print("======")
        print(item)
   


    


