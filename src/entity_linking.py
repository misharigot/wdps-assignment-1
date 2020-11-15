import json
from typing import List, Dict, Tuple

import requests
import trident
from elasticsearch import Elasticsearch
import asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_streaming_bulk


class Entity_Linking:
    # The minimum popularity for an entity to be linked
    MIN_POPULARITY = 5

    def __init__(self, KBPATH):
        # self.e = Elasticsearch([{"host": "localhost", "port": 9200}], timeout=5)
        self.es = AsyncElasticsearch([{"host": "localhost", "port": 9200}], timeout=30)
        self.db = trident.Db(KBPATH)
        self.loop = asyncio.get_event_loop()
        self.cache: Dict[str, str] = {}

    async def asyncSearch(self, entity):
        response = await self.es.search(
            index="wikidata_en",
            body={
                "query": {
                    "query_string": {
                        "query": entity,
                        "default_operator": "AND",
                        "type": "phrase",
                        "default_field": "schema_name",
                    }
                }
            },
            size=200,
        )
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

    async def asyncBulkSearch(self, entities):
        for i in range(0, len(entities)):
            for x in range(0, 20):
                await asyncio.create_task(self.asyncSearch(entities[i] + str(x)))
            print("result" + str(i))

    async def close(self):
        await self.es.close()

    # def searchElastic(self, query):
    #     p = {
    #         "query": {
    #             "query_string": {
    #                 "query": query,
    #                 "default_operator": "AND",
    #                 "type": "phrase",
    #                 "default_field": "schema_name"
    #             }
    #         }
    #     }

    #     response = self.e.search(index="wikidata_en", body=json.dumps(p), size=200)
    #     # idea maybe query name and a.k.a. instead of name and description (possibly faster more accurate since we often have the abbreviation)
    #     id_labels = {}
    #     if response:
    #         for hit in response["hits"]["hits"]:
    #             try:
    #                 # same entity have schema name missing
    #                 label = hit["_source"]["schema_name"]
    #             except Exception as e:
    #                 continue
    #             id = hit["_id"]
    #             # could also retrieve the ES score here
    #             id_labels.setdefault(id, set()).add(label)
    #     return id_labels

    def _push_to_cache(self, entity, wikidata_url):
        self.cache[entity] = wikidata_url

    def entity_linking(self, entities: List[str]) -> List[Tuple[str, str]]:
        result = self.loop.run_until_complete(self.entityLinking(entities))

        # loop.run_until_complete(self.close())
        # loop.close()
        # asyncio.run(self.close())
        return result

    #!!a bit confusing but i use _ to anotate tuples, where the left side of _ means the first item in the tuple!!
    async def entityLinking(self, entities: List[str]):
        linked_entities = []  # (entity, wikidata)
        for entity in entities:
            # Check cache
            cached_wikidata_url = self.cache.get(entity)
            if cached_wikidata_url is not None:  # exists in cache
                most_popular_entity = (entity, cached_wikidata_url)
                linked_entities.append(most_popular_entity)
            else:
                most_popular_entity = await self._get_most_popular_entity(entity)
                if most_popular_entity is None:
                    continue
                wikidata_url = most_popular_entity[1]
                self._push_to_cache(entity, wikidata_url)
                linked_entities.append(most_popular_entity)
        return linked_entities

    async def _get_most_popular_entity(self, entity):
        highest_popularity = self.MIN_POPULARITY
        most_popular_wikidata_url = None
        try:
            id_labels = await asyncio.create_task(self.asyncSearch(entity))
            for wikidata_url, label in id_labels.items():
                wikidata_ref = self.db.lookup_id(wikidata_url)
                popularity = self.db.count_o(wikidata_ref)
                if popularity > highest_popularity:
                    most_popular_wikidata_url = wikidata_url
                    highest_popularity = popularity
        except Exception as e:  # If a timeout occurs, skip the entity
            # print(f"Cannot processes {entity[1]}", e)
            return None

        if most_popular_wikidata_url is None:
            return None

        return (entity, most_popular_wikidata_url)

    def __del__(self):
        self.loop.run_until_complete(self.close())
        self.loop.close()