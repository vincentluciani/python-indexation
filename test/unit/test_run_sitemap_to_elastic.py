import runpy
from pathlib import Path
from unittest.mock import patch


def test_run_sitemap_to_elastic_transforms_tutorial_url_and_sends_documents():
    # ../src/run_sitemap_to_elastic.py 
    script_path = Path(__file__).resolve().parents[2] / "src" / "run_sitemap_to_elastic.py"
     
    def fake_parse_stream_from_url(url, compression, parser_type, json_args):
        if parser_type == "xml":
            return iter(["https://www.example.com/tutorial/page1"])
        if parser_type == "html_tables":
            return iter([
                [
                    {
                        "table_title": "FAQ",
                        "columns_values": ["Question?", "Answer."],
                    }
                ]
            ])
        return iter([])

    with patch("src.extract_information.parse_stream_from_url.parse_stream_from_url", side_effect=fake_parse_stream_from_url) as mock_parse, \
         patch("src.send_information.data_senders.send_data_to_elastic.send_list_of_documents_to_elastic") as mock_send, \
         patch("builtins.print"):
        runpy.run_path(str(script_path), run_name="__main__")

        mock_parse.assert_any_call(
            "https://www.vincent-luciani.com/sitemap.xml.gz",
            "gzip",
            "xml",
            {"parent_tag": "url", "child_tag": "loc"},
        )
        mock_parse.assert_any_call(
            "https://www.example.com/tutorial/page1",
            "none",
            "html_tables",
            {"title_tag": "h2"},
        )
        mock_send.assert_called_once_with(
            [
                {
                    "category": "tutorial",
                    "sub_category": "FAQ",
                    "question": "Question?",
                    "answer": "Answer.",
                }
            ],
            "vince",
        )


def test_run_sitemap_to_elastic_skips_non_tutorial_urls_and_does_not_send():
    script_path = Path(__file__).resolve().parents[2] / "src" / "run_sitemap_to_elastic.py"

    with patch("src.extract_information.parse_stream_from_url.parse_stream_from_url", return_value=iter(["https://www.example.com/page1"])) as mock_parse, \
         patch("src.send_information.data_senders.send_data_to_elastic.send_list_of_documents_to_elastic") as mock_send, \
         patch("builtins.print"):
        runpy.run_path(str(script_path), run_name="__main__")

        mock_parse.assert_called_once()
        mock_send.assert_not_called()
