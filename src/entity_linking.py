import requests
import json
from elasticsearch import Elasticsearch
import trident

KBPATH='./../assets/wikidata-20200203-truthy-uri-tridentdb'
# Load the KB
db = trident.Db(KBPATH)

#0 start with list of entities and their type
entities = [
        # ("ORGANIZATION", "NLP"),
        # ("PERSON", "Richard Bandler"),
        # ("PERSON", "John Grinder"),
        # ("GPE", "California"),
        ("ORGANIZATION", "Google"),
        # ("GPE", "United States")        
    ]

def searchElastic(query):
    e = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    p = {"query": {"query_string": {"query": query}}}
    response = e.search(index="wikidata_en", body=json.dumps(p))
    #idea maybe query name and a.k.a. instead of name and description (possibly faster more accurate since we often have the abbreviation)
    id_labels = {}
    if response:
        for hit in response["hits"]["hits"]:
            label = hit["_source"]["schema_name"]
            id = hit["_id"]
            #could also retrieve the ES score here
            id_labels.setdefault(id, set()).add(label)
    return id_labels

def searchTrident(query):
    query="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s where { ?s wdp:P31 wde:Q515 . } LIMIT 10"
    results = db.sparql(query)
    json_results = json.loads(results)
    return json_results["results"]

def entityLinking(entity_type):
    entity_wikidata = [] #(entity, wikidata)
    for entity in entity_type:
        entitiy_popularity = [] #(entity, popularity)
        #1look in elasticsearch for wikidate references per entity
        for wikidata_url, label in searchElastic(entity[1]).items():
            #for exampe now query trident and retreive the most popular (most references) wikipedia article for the entity
            #MVP: use score and popularity
            #2 retrieve info from trident
            wikidata_ref = db.lookup_id(wikidata_url)
            popularity = db.count_o(wikidata_ref)
            entitiy_popularity.append((wikidata_url, popularity))
            #TODO: better would be to use context dependent 
        #3 identify the best possible match
        entitiy_popularity.sort(key=lambda x: x[1], reverse=True)
        entity_wikidata.append((entity[1],entitiy_popularity[0][0]))
    return entity_wikidata

if __name__ == "__main__":
    entity_wikidata = entityLinking(entities)
    print(entity_wikidata)


            