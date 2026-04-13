"""Send document batches to Elasticsearch via HTTP bulk API."""

import json
import os
from elastic_setup.execute_http import execute_http_request


def send_list_of_documents_to_elastic(document_list, index_name):
    """Send a list of documents to Elasticsearch."""
    bulk_data = build_bulk_upload_entry(document_list, index_name)
    send_data_to_elastic(bulk_data, index_name)


def send_data_to_elastic(input_data, index_name):
    """Post bulk data to Elasticsearch using configured credentials."""
    user = os.getenv("ELASTIC_USER", "elastic")
    password = os.getenv("ELASTIC_PASSWORD")
    elasticsearch_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    url = f"{elasticsearch_url}/{index_name}/_bulk"
    headers = {"Content-Type": "application/x-ndjson"}
    execute_http_request(
        "POST",
        url,
        user,
        password,
        data_binary=input_data,
        headers=headers,
    )


def build_bulk_upload_entry(list_of_value_pairs, index_name):
    """Build an Elasticsearch NDJSON bulk upload payload."""
    final_bulk_data = ""
    for document in list_of_value_pairs:
        value_pair_json = dict(document)
        header = f'{{"index":{{"_index":"{index_name}"}}}}\n'
        final_bulk_data += f"{header}{json.dumps(value_pair_json)}\n"
    return final_bulk_data
