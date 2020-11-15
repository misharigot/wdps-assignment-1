"""Link a list of entities to their Wikidata URL using Elasticsearch and Trident.
"""

import asyncio
import json
from typing import Dict, List, Tuple, Optional

import requests
import trident
from elasticsearch import AsyncElasticsearch, Elasticsearch
from elasticsearch.helpers import async_streaming_bulk


class Entity_Linking:
    # The minimum popularity for an entity to be linked
    MIN_POPULARITY = 5

    def __init__(self, KBPATH: str):
        self.es = AsyncElasticsearch([{"host": "localhost", "port": 9200}], timeout=30)
        self.db = trident.Db(KBPATH)
        self.loop = asyncio.get_event_loop()
        self.cache: Dict[str, str] = {}

    async def _async_search(self, entity: str) -> Dict[str, str]:
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

    async def close_es(self):
        await self.es.close()

    def _push_to_cache(self, entity: str, wikidata_url: str):
        self.cache[entity] = wikidata_url

    def entity_linking(self, entities: List[str]) -> List[Tuple[str, str]]:
        result = self.loop.run_until_complete(self._link_entities_async(entities))
        return result

    async def _link_entities_async(self, entities: List[str]) -> List[Tuple[str, str]]:
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

    async def _get_most_popular_entity(self, entity: str) -> Optional[Tuple[str, str]]:
        highest_popularity = self.MIN_POPULARITY
        most_popular_wikidata_url = None
        try:
            id_labels = await asyncio.create_task(self._async_search(entity))
            for wikidata_url, label in id_labels.items():
                wikidata_ref = self.db.lookup_id(wikidata_url)
                popularity = self.db.count_o(wikidata_ref)
                if popularity > highest_popularity:
                    most_popular_wikidata_url = wikidata_url
                    highest_popularity = popularity
        except Exception as e:  # If an exception occurs, skip entity.
            return None

        if most_popular_wikidata_url is None:
            return None

        return (entity, most_popular_wikidata_url)

    def __del__(self):
        self.loop.run_until_complete(self.close_es())
        self.loop.close()
