import entity_linking as el
from elasticsearch import Elasticsearch

KBPATH = "assets/wikidata-20200203-truthy-uri-tridentdb"
entity_linking = el.Entity_Linking(KBPATH)

# to run these tests elasticsearch should be running

# def test_searchTrident():
#     assert 1 ==1


def test_searchElastic():
    entity = ("ORGANIZATION", "Vrije Universiteit Amsterdam")
    actual = entity_linking.searchElastic(entity[1])
    expected = {
        "<http://www.wikidata.org/entity/Q70764476>": (
            "Vrije Universiteit Amsterdam",
            '[The hospital of the \\"Vrije Universiteit\\" in Amsterdam]',
            "scientific article published on 01 November 1966",
        ),
        "<http://www.wikidata.org/entity/Q2610973>": (
            "Vrije Universiteit Amsterdam",
            "Hortus Botanicus Vrije Universiteit Amsterdam",
            "botanical garden belonging to Vrije Universiteit in Amsterdam",
        ),
        "<http://www.wikidata.org/entity/Q61671111>": (
            "Vrije Universiteit Amsterdam",
            "Faculteit der Rechtsgeleerdheid",
            "Vrije Universiteit Amsterdam",
        ),
        "<http://www.wikidata.org/entity/Q1065414>": (
            "Vrije Universiteit Amsterdam",
            "Vrije Universiteit",
            "university in Amsterdam, The Netherlands",
        ),
        "<http://www.wikidata.org/entity/Q44098890>": (
            "Vrije Universiteit Amsterdam",
            "Peter Mika",
            "researcher, Vrije Universiteit Amsterdam",
        ),
        "<http://www.wikidata.org/entity/Q65937341>": (
            "Vrije Universiteit Amsterdam",
            "Pia Sommerauer",
            "researcher, Vrije Universiteit Amsterdam",
        ),
        "<http://www.wikidata.org/entity/Q58894745>": (
            "Vrije Universiteit Amsterdam",
            "Victor de Boer",
            "researcher, Vrije Universiteit Amsterdam",
        ),
        "<http://www.wikidata.org/entity/Q612665>": (
            "Vrije Universiteit Amsterdam",
            "Vrije Universiteit Brussel",
            "University in Brussels",
        ),
    }
    assert expected == actual


def test_entityLinking():
    entities = [("ORGANIZATION", "Google")]
    entity_wikidata = entity_linking.entityLinking(entities)
    expected = [("Google", "<http://www.wikidata.org/entity/Q95>")]
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
        ("DATE", "the 1970s"),
    ]
    entity_wikidata = entity_linking.entityLinking(entities)
    expected = 28
    assert expected == len(entity_wikidata)
