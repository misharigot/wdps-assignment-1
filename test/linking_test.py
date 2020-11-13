import entity_linking as el
from elasticsearch import Elasticsearch

KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'
entity_linking = el.Entity_Linking(KBPATH)

#to run these tests elasticsearch should be running

# def test_searchTrident():
#     assert 1 ==1

def test_searchElastic():
    entity = ("ORGANIZATION", "Vrije Universiteit Amsterdam")
    wikiurl_wikilabel = entity_linking.searchElastic(entity[1])
    expected= {'<http://www.wikidata.org/entity/Q70764476>': {'[The hospital of the \\"Vrije Universiteit\\" in Amsterdam]'},
     '<http://www.wikidata.org/entity/Q2610973>': {'Hortus Botanicus Vrije Universiteit Amsterdam'},
     '<http://www.wikidata.org/entity/Q71001152>': {'4.4. Starting New Data Conversations at Vrije Universiteit Amsterdam'},
     '<http://www.wikidata.org/entity/Q61671111>': {'Faculteit der Rechtsgeleerdheid'},
     '<http://www.wikidata.org/entity/Q1065414>': {'Vrije Universiteit'},
     '<http://www.wikidata.org/entity/Q44098890>': {'Peter Mika'},
     '<http://www.wikidata.org/entity/Q65937341>': {'Pia Sommerauer'},
     '<http://www.wikidata.org/entity/Q58894745>': {'Victor de Boer'},
     '<http://www.wikidata.org/entity/Q2187167>': {'Vrije Universiteit Amsterdam. Centrum voor Nederlandse Religiegeschiedenis'},
     '<http://www.wikidata.org/entity/Q612665>': {'Vrije Universiteit Brussel'}}
    print(wikiurl_wikilabel)
    assert expected == wikiurl_wikilabel

def test_entityLinking():
    entities = [
        ("ORGANIZATION", "Google")
    ]
    entity_wikidata = entity_linking.entityLinking(entities)
    expected= [('Google', '<http://www.wikidata.org/entity/Q95>')]
    assert expected == entity_wikidata

def test_entityLinkingBatch():
    entities = [
        ("ORG", "Neuro"),
        ("ORG", "NLP"),
        ("PERSON", "Richard Bandler"),
        ("PERSON", "John Grinder"),
        ("GPE", "California"),
        ("GPE", "United States"),
        ("DATE", "the 1970s"),
        ("ORG", "Neuro"),
        ("ORG", "NLP"),
        ("PERSON", "Richard Bandler"),
        ("PERSON", "John Grinder"),
        ("GPE", "California"),
        ("GPE", "United States"),
        ("DATE", "the 1970s"),
        ("ORG", "Neuro"),
        ("ORG", "NLP"),
        ("PERSON", "Richard Bandler"),
        ("PERSON", "John Grinder"),
        ("GPE", "California"),
        ("GPE", "United States"),
        ("DATE", "the 1970s"),
        ("ORG", "Neuro"),
        ("ORG", "NLP"),
        ("PERSON", "Richard Bandler"),
        ("PERSON", "John Grinder"),
        ("GPE", "California"),
        ("GPE", "United States"),
        ("DATE", "the 1970s")
    ]
    entity_wikidata = entity_linking.entityLinking(entities)
    expected= 28
    assert expected == len(entity_wikidata)