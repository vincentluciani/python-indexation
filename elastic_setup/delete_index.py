
import os

from execute_http import execute_http_request, print_response

user =  os.getenv("ELASTIC_USER","elastic")
password = os.getenv("ELASTIC_PASSWORD")
URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

print("==========> Removing the index 'vince'...")
response = execute_http_request("DELETE", URL + "/vince", user, password,json_body=None, headers=None)
print_response(response)

