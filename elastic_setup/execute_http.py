import json
import requests

def execute_http_request(method, url, user, password,json_body=None, headers=None):

    if not user or not password:
        raise ValueError("Missing user or password for authentication")

    response = requests.request(
        method=method.upper(),
        url=url,
        auth=(user, password),
        verify=False,      # skip SSL verification if self-signed
        headers=headers,
        json=json_body     # automatically converts dict to JSON
    )

    response.raise_for_status()  # raises exception if 4xx or 5xx
    return response

def print_response(response):
    data = response.json()
    print(json.dumps(data, indent=2))
