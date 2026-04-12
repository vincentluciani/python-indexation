from unittest.mock import MagicMock, patch

from src.transform_information.transform_with_ai import summarize_with_ai


def test_summarize_with_ai_builds_messages_and_returns_content():
    fake_response = {"message": {"content": "result text"}}
    fake_client = MagicMock()
    fake_client.chat.return_value = fake_response

    with patch("src.transform_information.transform_with_ai.ollama.Client", return_value=fake_client) as mock_client:
        result = summarize_with_ai(
            "phi3:mini",
            ["first item", "second item"],
            "system prompt",
            "Customer Suggestions",
        )

    mock_client.assert_called_once_with(host="http://localhost:11434")
    fake_client.chat.assert_called_once_with(
        model="phi3:mini",
        messages=[
            {"role": "system", "content": "system prompt"},
            {"role": "user", "content": "Customer Suggestions:\n- first item\n- second item"},
        ],
        options={"temperature": 0},
    )
    assert result == "result text"


def test_summarize_with_ai_returns_empty_string_when_no_message():
    fake_client = MagicMock()
    fake_client.chat.return_value = {}

    with patch("src.transform_information.transform_with_ai.ollama.Client", return_value=fake_client):
        result = summarize_with_ai("phi3:mini", [], "system prompt", "prefix")

    assert result == ""
