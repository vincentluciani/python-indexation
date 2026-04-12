import runpy
from pathlib import Path
from unittest.mock import ANY, patch


def test_run_ai_ollama_enrichment_executes_and_calls_summarize_with_expected_requests():
    script_path = Path(__file__).resolve().parents[2] / "src" / "run_ai_ollama_enrichment.py"

    with patch("src.extract_information.parse_stream_from_file.parse_stream_from_file") as mock_parse, \
         patch("src.transform_information.transform_with_ai.summarize_with_ai") as mock_summarize, \
         patch("builtins.print") as mock_print:
        mock_parse.return_value = [[
            ["ignored", "request one"],
            ["ignored", "request two"],
        ]]
        mock_summarize.return_value = "Summary result"

        runpy.run_path(str(script_path), run_name="__main__")

        mock_summarize.assert_called_once_with(
            "phi3:mini",
            ["request one", "request two"],
            ANY,
            "Customer Suggestions",
        )

        assert any(
            call.args and call.args[0] == "calling summarize_with_ai..."
            for call in mock_print.call_args_list
        )


def test_run_ai_ollama_enrichment_uses_parse_stream_results_to_build_list():
    script_path = Path(__file__).resolve().parents[2] / "src" / "run_ai_ollama_enrichment.py"

    with patch("src.extract_information.parse_stream_from_file.parse_stream_from_file") as mock_parse, \
         patch("src.transform_information.transform_with_ai.summarize_with_ai") as mock_summarize:
        mock_parse.return_value = [[
            ["a", "first"],
            ["b", "second"],
            ["c", "third"],
        ]]
        mock_summarize.return_value = "done"

        runpy.run_path(str(script_path), run_name="__main__")

        mock_summarize.assert_called_once()
        _, kwargs = mock_summarize.call_args
        assert kwargs == {}
        assert mock_summarize.call_args[0][1] == ["first", "second", "third"]
