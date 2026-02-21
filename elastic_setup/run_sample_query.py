#!/bin/bash
import os

from execute_http import  execute_http_request, print_response

user = os.getenv("ELASTIC_USER","elastic")
password = os.getenv("ELASTIC_PASSWORD")
elasticsearch_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
URL = f"{elasticsearch_url}/vince/_search?q=array"
headers = {'Content-Type': 'application/json'}

    
response = execute_http_request("GET", URL, user, password,headers=headers)
print_response(response)

