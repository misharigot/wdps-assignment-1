import requests
import json
from elasticsearch import Elasticsearch


def search(query):
    e = Elasticsearch([{"host": "localhost", "port": 9200}])
    p = {"query": {"query_string": {"query": query}}}
    response = e.search(index="wikidata_en", body=json.dumps(p))
    id_labels = {}
    if response:
        for hit in response["hits"]["hits"]:
            try:
                # same entity have schema name missing
                label = hit["_source"]["schema_name"]
            except Exception as e:
                continue
            id = hit["_id"]
            id_labels.setdefault(id, set()).add(label)
    return id_labels


if __name__ == "__main__":
    import sys

    try:
        _, QUERY = sys.argv
    except Exception as e:
        QUERY = "Vrije Universiteit Amsterdam"

    for entity, labels in search(QUERY).items():
        print(entity, labels)
