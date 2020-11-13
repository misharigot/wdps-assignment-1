import json
from typing import List

import requests
import trident
from elasticsearch import Elasticsearch


class Entity_Linking:
    def __init__(self, KBPATH):
        self.e = Elasticsearch([{"host": "localhost", "port": 9200}], timeout=30)
        self.db = trident.Db(KBPATH)

    def searchElastic(self, query):
        p = {"query": {"query_string": {"query": query}}}
        response = self.e.search(index="wikidata_en", body=json.dumps(p), size=10)
        # idea maybe query name and a.k.a. instead of name and description (possibly faster more accurate since we often have the abbreviation)
        id_labels = {}
        if response:
            for hit in response["hits"]["hits"]:
                try:
                    # same entity have schema name missing
                    label = hit["_source"]["schema_name"]
                except Exception as e:
                    continue
                id = hit["_id"]
                # could also retrieve the ES score here
                id_labels.setdefault(id, set()).add(label)
        return id_labels

    #!!a bit confusing but i use _ to anotate tuples, where the left side of _ means the first item in the tuple!!
    def entityLinking(self, entities: List[str]):
        entity_wikidata = []  # (entity, wikidata)
        for entity in entities:
            # print("searching elastic for entity: " + entity[1])
            entity_popularity = []  # (entity, popularity)
            # Look in elasticsearch for wikidate references per entity
            try:
                for wikidata_url, label in self.searchElastic(entity).items():
                    # for example now query trident and retreive the most popular (most references) wikipedia article for the entity
                    # MVP: use score and popularity
                    # 2 retrieve info from trident
                    wikidata_ref = self.db.lookup_id(wikidata_url)
                    popularity = self.db.count_o(wikidata_ref)

                    # e.g. [('<http://www.wikidata.org/entity/Q271982>', 11)]
                    entity_popularity.append((wikidata_url, popularity))

            except Exception as e: # If a timeout occurs, skip the entity
                # print(f"Cannot processes {entity[1]}", e)
                continue

            if not entity_popularity:
                # print("list is empty")
                continue

            # print("elastic returned amount of results: " + str(len(entity_popularity)))
            entity_popularity.sort(key=lambda x: x[1], reverse=True)
            entity_wikidata.append((entity, entity_popularity[0][0]))
            # print("best match was: " + entity_popularity[0][0])
        return entity_wikidata
