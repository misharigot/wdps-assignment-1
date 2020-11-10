import requests
import json
from elasticsearch import Elasticsearch
import trident

class Entity_Linking:
    def __init__(self, KBPATH):
        self.e = Elasticsearch([{'host': 'localhost', 'port': 9200}],timeout=30)
        self.db = trident.Db(KBPATH)

    def searchElastic(self, query):    
        p = {"query": {"query_string": {"query": query}}}
        response = self.e.search(index="wikidata_en", body=json.dumps(p), size=10)
        #idea maybe query name and a.k.a. instead of name and description (possibly faster more accurate since we often have the abbreviation)
        id_labels = {}
        if response:
            for hit in response["hits"]["hits"]:
                try:
                    #same entity have schema name missing
                    label = hit["_source"]["schema_name"]
                except Exception as e:
                    continue
                id = hit["_id"]
                #could also retrieve the ES score here
                id_labels.setdefault(id, set()).add(label)
        return id_labels

    def searchTrident(self,query):
        query="PREFIX wde: <http://www.wikidata.org/entity/> "\
            "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
            "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
            "select ?s where { ?s wdp:P31 wde:Q515 . } LIMIT 10"
        results = db.sparql(query)
        json_results = json.loads(results)
        return json_results["results"]

    #!!a bit confusing but i use _ to anotate tuples, where the left side of _ means the first item in the tuple!!
    def entityLinking(self, entitytype_entities):
        entity_wikidata = [] #(entity, wikidata)
        for entitytype_entity in entitytype_entities:
            entitiy_popularity = [] #(entity, popularity)
            #1look in elasticsearch for wikidate references per entity
            for wikidata_url, label in self.searchElastic(entitytype_entity[1]).items():
                #for exampe now query trident and retreive the most popular (most references) wikipedia article for the entity
                #MVP: use score and popularity
                #2 retrieve info from trident
                wikidata_ref = self.db.lookup_id(wikidata_url)
                popularity = self.db.count_o(wikidata_ref)
                entitiy_popularity.append((wikidata_url, popularity)) #e.g. [('<http://www.wikidata.org/entity/Q271982>', 11)]
                #TODO: better would be to use context dependent 
            #3 identify the best possible match
            entitiy_popularity.sort(key=lambda x: x[1], reverse=True)
            entity_wikidata.append((entitytype_entity[1],entitiy_popularity[0][0]))
        return entity_wikidata