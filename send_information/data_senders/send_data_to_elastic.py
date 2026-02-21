import json
import os
from elastic_setup.execute_http import execute_http_request
#vince
#knowledge

# TODO https://www.vincent-luciani.com/api/vince/knowledge/search/?term=test&pageSize=20
# what about knowledge ??
#router.get('/api/:country/:language/search/',executeQuery)
#Language is called knowledge in the url called, but it is not used in the code currently
def send_list_of_documents_to_elastic(document_list, index_name):
    bulk_data = build_bulk_upload_entry(document_list, index_name)
    send_data_to_elastic(bulk_data, index_name)

def build_bulk_upload_entry(document_list):
    final_bulk_data = ""
    for document in document_list:
        final_bulk_data += build_bulk_upload_entry(document)
    return final_bulk_data

def send_data_to_elastic(input_data, index_name):
    user =  os.getenv("ELASTIC_USER","elastic")
    password = os.getenv("ELASTIC_PASSWORD")
    elasticsearch_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    url = f"{elasticsearch_url}/{index_name}/_bulk"
    headers = {'Content-Type': 'application/x-ndjson'}
    execute_http_request("POST", url, user, password, data_binary=input_data, headers=headers)

def build_bulk_upload_entry(list_of_value_pairs, index_name):
    final_bulk_data = ""
    for document in list_of_value_pairs:
        value_pair_json = { key: json.dumps(value) for key, value in document.items() }
        header = f'{{"index":{{"_index":"{index_name}"}}}}\n'
        final_bulk_data += f'{header}{json.dumps(value_pair_json)}\n'
    return final_bulk_data

