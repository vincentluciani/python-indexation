
import os

from execute_http import execute_http_request, print_response

user =  os.getenv("ELASTIC_USER","elastic")
password = os.getenv("ELASTIC_PASSWORD")
URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
headers = {'Content-Type': 'application/json'}

print("==========> Checking Elasticsearch connection...")
response = execute_http_request("GET", URL, user, password,json_body=None, headers=headers)
print_response(response)

print("==========> Index settings for 'vince'")
response = execute_http_request("GET", URL + "/vince/_settings", user, password,json_body=None, headers=headers)
print_response(response)

print("==========> Index mappings for 'vince'")
response = execute_http_request("GET", URL + "/vince/_mapping", user, password,json_body=None, headers=headers)
print_response(response)


body = {  
  "analyzer": "simple_analyzer",
  "text": "remove the changes"
}

print("==========> Analyzer test: analyze 'test text' with simple_analyzer")
response = execute_http_request("POST", URL + "/vince/_analyze", user, password,json_body=body, headers=headers)
print_response(response)

