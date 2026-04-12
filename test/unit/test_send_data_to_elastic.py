import os
from unittest.mock import patch

from src.send_information.data_senders.send_data_to_elastic import (
    build_bulk_upload_entry,
    send_data_to_elastic,
    send_list_of_documents_to_elastic,
)


def test_build_bulk_upload_entry_formats_indexed_json():
    result = build_bulk_upload_entry(
        [
            {"title": "Hello", "value": "World"},
            {"foo": "bar"},
        ],
        "test-index",
    )

    assert result.startswith('{"index":{"_index":"test-index"}}\n')
    assert '{"title": "Hello", "value": "World"}\n' in result
    assert '{"foo": "bar"}\n' in result


def test_send_data_to_elastic_uses_environment_variables_and_http_request():
    with patch("src.send_information.data_senders.send_data_to_elastic.execute_http_request") as mock_request:
        with patch.dict(os.environ, {"ELASTIC_USER": "elastic", "ELASTIC_PASSWORD": "secret", "ELASTICSEARCH_URL": "http://custom:9200"}, clear=True):
            send_data_to_elastic("payload", "my-index")

        mock_request.assert_called_once_with(
            "POST",
            "http://custom:9200/my-index/_bulk",
            "elastic",
            "secret",
            data_binary="payload",
            headers={"Content-Type": "application/x-ndjson"},
        )


def test_send_list_of_documents_to_elastic_builds_bulk_and_sends():
    with patch("src.send_information.data_senders.send_data_to_elastic.send_data_to_elastic") as mock_send:
        send_list_of_documents_to_elastic(
            [{"a": "1"}, {"b": "2"}],
            "bulk-index",
        )

    assert mock_send.call_count == 1
    bulk_data, index_name = mock_send.call_args[0]
    assert index_name == "bulk-index"
    assert '{"index":{"_index":"bulk-index"}}\n' in bulk_data
    assert '{"a": "1"}\n' in bulk_data
    assert '{"b": "2"}\n' in bulk_data
