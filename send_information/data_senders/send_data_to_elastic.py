from elasticsearch import Elasticsearch

class ElasticSearchClient:
    def __init__(self, host, port, username, password):
        self.es = Elasticsearch(
            [f"https://{host}:{port}"],
            verify_certs=False,
            http_auth=(username, password)
        )

    def push_data_to_target(self,data):
        for entry in data:
            self.es.index(index="knowledge", document=entry)