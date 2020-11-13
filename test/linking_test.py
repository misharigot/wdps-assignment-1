import entity_linking as el
from elasticsearch import Elasticsearch

KBPATH = "assets/wikidata-20200203-truthy-uri-tridentdb"
entity_linking = el.Entity_Linking(KBPATH)

# to run these tests elasticsearch should be running

# def test_searchTrident():
#     assert 1 ==1


def test_searchElastic():
    entity = ("ORGANIZATION", "Vrije Universiteit Amsterdam")
    wikiurl_wikilabel = entity_linking.searchElastic(entity[1])
    expected = {
        "<http://www.wikidata.org/entity/Q70764476>": {
            '[The hospital of the \\"Vrije Universiteit\\" in Amsterdam]'
        },
        "<http://www.wikidata.org/entity/Q2610973>": {
            "Hortus Botanicus Vrije Universiteit Amsterdam"
        },
        "<http://www.wikidata.org/entity/Q71001152>": {
            "4.4. Starting New Data Conversations at Vrije Universiteit Amsterdam"
        },
        "<http://www.wikidata.org/entity/Q61671111>": {
            "Faculteit der Rechtsgeleerdheid"
        },
        "<http://www.wikidata.org/entity/Q1065414>": {"Vrije Universiteit"},
        "<http://www.wikidata.org/entity/Q44098890>": {"Peter Mika"},
        "<http://www.wikidata.org/entity/Q65937341>": {"Pia Sommerauer"},
        "<http://www.wikidata.org/entity/Q58894745>": {"Victor de Boer"},
        "<http://www.wikidata.org/entity/Q2187167>": {
            "Vrije Universiteit Amsterdam. Centrum voor Nederlandse Religiegeschiedenis"
        },
        "<http://www.wikidata.org/entity/Q612665>": {"Vrije Universiteit Brussel"},
    }
    assert expected == wikiurl_wikilabel


def test_entityLinking():
    entities = ["Google"]
    entity_wikidata = entity_linking.entityLinking(entities)
    expected = [("Google", "<http://www.wikidata.org/entity/Q95>")]
    assert expected == entity_wikidata


def test_entityLinkingBatch():
    entities = [
        "Neuro",
        "NLP",
        "Richard Bandler",
        "John Grinder",
        "California",
        "United States",
        "the 1970s",
        "Neuro",
        "NLP",
        "Richard Bandler",
        "John Grinder",
        "California",
        "United States",
        "the 1970s",
        "Neuro",
        "NLP",
        "Richard Bandler",
        "John Grinder",
        "California",
        "United States",
        "he 1970s",
        "Neuro",
        "NLP",
        "Richard Bandler",
        "John Grinder",
        "California",
        "United States",
        "the 1970s",
    ]
    entity_wikidata = entity_linking.entityLinking(entities)
    expected = 28
    assert expected == len(entity_wikidata)


def test_entityLinking_from_cache():
    entity_linking = el.Entity_Linking(KBPATH)  # Free cache by making new object
    first_entities = ["Richard Bandler", "Bob Ross"]

    second_entities = ["Richard Bandler", "Joe Biden"]
    first_expected = [
        ("Richard Bandler", "<http://www.wikidata.org/entity/Q452751>"),
        ("Bob Ross", "<http://www.wikidata.org/entity/Q455511>"),
    ]
    second_expected = [
        ("Richard Bandler", "<http://www.wikidata.org/entity/Q452751>"),
        ("Joe Biden", "<http://www.wikidata.org/entity/Q6279>"),
    ]

    assert entity_linking.cache.get("Richard Bandler") is None
    first_linked_entities = entity_linking.entityLinking(first_entities)
    assert entity_linking.cache.get("Richard Bandler") is not None

    # Should get Richard Bandler from cache here
    second_linked_entities = entity_linking.entityLinking(second_entities)

    assert first_linked_entities == first_expected
    assert second_linked_entities == second_expected
