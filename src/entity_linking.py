import requests
import json
from elasticsearch import Elasticsearch
import trident
from typing import List, Tuple, Dict


class Entity_Linking:
    def __init__(self, KBPATH, strategy="query_string"):
        self.e = Elasticsearch([{"host": "localhost", "port": 9200}], timeout=30)
        self.db = trident.Db(KBPATH)
        self.strategy = strategy

    def searchElastic(self, query):
        if self.strategy == "match":
            p = {"query": {"match": {"message": {"query": query}}}}
        else:
            p = {"query": {"query_string": {"query": query}}}
        response = self.e.search(index="wikidata_en", body=json.dumps(p), size=10)
        # idea maybe query name and a.k.a. instead of name and description (possibly faster more accurate since we often have the abbreviation)
        results = {}
        if response:
            for hit in response["hits"]["hits"]:
                try:
                    # same entity have schema name missing
                    name = hit["_source"]["schema_name"]
                    description = hit["_source"]["schema_description"]
                except Exception as e:
                    continue
                _id = hit["_id"]
                # could also retrieve the ES score here
                # id_labels.setdefault(id, set()).add(label)
                label = query
                results[_id] = (label, name, description)
        return results

    #!!a bit confusing but i use _ to anotate tuples, where the left side of _ means the first item in the tuple!!
    def entityLinking(self, entitytype_entities):
        entity_wikidata = []  # (entity, wikidata)
        for entitytype_entity in entitytype_entities:
            entity_popularity = []  # (entity, popularity)
            # 1look in elasticsearch for wikidate references per entity
            for wikidata_url, label in self.searchElastic(entitytype_entity[1]).items():
                # for exampe now query trident and retreive the most popular (most references) wikipedia article for the entity
                # MVP: use score and popularity
                # 2 retrieve info from trident
                wikidata_ref = self.db.lookup_id(wikidata_url)
                popularity = self.db.count_o(wikidata_ref)
                entity_popularity.append(
                    (wikidata_url, popularity)
                )  # e.g. [('<http://www.wikidata.org/entity/Q271982>', 11)]
                # TODO: better would be to use context dependent
            # 3 identify the best possible match
            if not entity_popularity:
                continue
            entity_popularity.sort(key=lambda x: x[1], reverse=True)
            entity_wikidata.append((entitytype_entity[1], entity_popularity[0][0]))
        return entity_wikidata

    def enrich_entities(self, entities) -> List[Dict[str, Tuple[str, str, str]]]:
        enriched_entities = []
        for entity in entities:
            entity_name: str = entity[1]
            enriched_entities.append(self.searchElastic(entity_name))
        return enriched_entities
