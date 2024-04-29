from elasticsearch import Elasticsearch
import time


class ES:
    def __init__(self, index) -> None:
        self.es = Elasticsearch(hosts=["http://elasticsearch:9200"])
        while not self.es.ping():
            self.es = Elasticsearch(hosts=["http://elasticsearch:9200"])
            print('RECONNECTING TO ElasticSearch...')
            time.sleep(10)
        self.index = index
        indices = self.es.indices.get_alias()
        if index not in indices:
            self.es.indices.create(index=index)


    def search_document(self, text, field):
        query = {
            "query": {
                "match": {
                    field: {
                        "query": text,
                        "fuzziness": "AUTO"
                    }
                }
            }
        }
        result = self.es.search(index=self.index, body=query)
        return result


    def add_document(self, document):
        response = self.es.index(index=self.index, body=document)

        return response
