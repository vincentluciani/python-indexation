import os

from execute_http import execute_http_request, print_response

user = os.getenv("ELASTIC_USER")
password = os.getenv("ELASTIC_PASSWORD")
URL = "http://localhost:9200"
headers = {'Content-Type': 'application/json'}

print("==========> Checking Elasticsearch cluster health...")
response = execute_http_request("GET", URL, user, password,json_body=None, headers=headers)
print_response(response)
