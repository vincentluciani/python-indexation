import os

from execute_http import  execute_http_request

user = os.getenv("ELASTIC_USER")
password = os.getenv("ELASTIC_PASSWORD")
URL = "http://localhost:9200/vince"
headers = {'Content-Type': 'application/json'}
body ={
          "settings": {
            "analysis": {
              "analyzer": {
                "my_analyzer": {"tokenizer": "my_tokenizer"},
                "simple_analyzer": {"tokenizer":"standard","filter":["synonym","stemmer","uppercase","my_custom_stop_words_filter"]}
              },
              "tokenizer": {
                "my_tokenizer": {"type": "ngram","min_gram":3,"max_gram":3,"token_chars":["letter","digit"]}
              },
              "filter": {
                "my_custom_stop_words_filter": {"type":"stop","ignore_case":True,"stopwords":["a","is","the"]},
                "synonym": {"type":"synonym","lenient":True,"synonyms":["remove,delete","change,modify"]}
              }
            }
          },
          "mappings": {
            "properties": {
              "category": {"type": "keyword"},
              "subCategory": {"type": "keyword"},
              "question": {"type": "text", "analyzer":"simple_analyzer"},
              "answer": {"type": "text", "analyzer":"simple_analyzer"}
            }
          }
        }
    
execute_http_request("PUT", URL, user, password,json_body=body, headers=headers)