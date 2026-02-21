import json
import requests

def execute_http_request(method, url, user, password,data_binary=None,json_body=None, headers=None):

    if not user or not password:
        raise ValueError("Missing user or password for authentication")

    binary_payload = data_binary if data_binary else None
    json_payload = json_body if not data_binary else None

    response = requests.request(
        method=method.upper(),
        url=url,
        auth=(user, password),
        verify=False,      # skip SSL verification if self-signed
        headers=headers,
        json=json_payload,   # automatically converts dict to JSON
        data=binary_payload    # for binary data, pass as-is
    )

    response.raise_for_status()  # raises exception if 4xx or 5xx
    return response

def print_response(response):
    data = response.json()
    print(json.dumps(data, indent=2))
