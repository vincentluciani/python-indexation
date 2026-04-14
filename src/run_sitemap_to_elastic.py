"""Run sitemap ingestion and index tutorial table data into Elasticsearch."""

from src.extract_information.parse_stream_from_url import parse_stream_from_url
from src.send_information.data_senders.send_data_to_elastic import (
    send_list_of_documents_to_elastic,
)
from src.read_configuration.read_configuration import load_yaml_config


if __name__ == "__main__":
    config = load_yaml_config("sitemap_to_elastic")
    parsing_args = config.get("source", {})
    print("========= Parsing arguments =========")
    print(parsing_args)
    for url_to_parse in parse_stream_from_url(parsing_args):
        print("======")
        resulting_learning_table = []
        if "tutorial" in url_to_parse:
            print("Found tutorial URL:", url_to_parse)
            parsing_args_tutorial = config.get("secondary_source", {})
            parsing_args_tutorial["location"] = url_to_parse

            for item in parse_stream_from_url(parsing_args_tutorial):
                transformed_item = [
                    {
                        "category": url_to_parse.split("/")[3],
                        "subCategory": x.get("table_title", "N/A"),
                        "question": (
                            x.get("columns_values", ["N/A"])[0]
                            if len(x.get("columns_values", [])) > 1
                            else "N/A"
                        ),
                        "answer": (
                            x.get("columns_values", ["N/A"])[1]
                            if len(x.get("columns_values", [])) > 1
                            else "N/A"
                        ),
                    }
                    for x in item
                ]
                resulting_learning_table.append(transformed_item)

            number_of_rows = sum(len(item) for item in resulting_learning_table)
            print(f"url: {url_to_parse}")
            print(
                f"Total number of rows in the resulting learning table: "
                f"{number_of_rows}"
            )
            send_list_of_documents_to_elastic(resulting_learning_table[0], "vince")
