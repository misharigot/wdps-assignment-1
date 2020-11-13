import entity_linking as el
from elasticsearch import Elasticsearch

KBPATH = "assets/wikidata-20200203-truthy-uri-tridentdb"
entity_linking = el.Entity_Linking(KBPATH)

# to run these tests elasticsearch should be running

# def test_searchTrident():
#     assert 1 ==1


def test_searchElastic():
    result = entity_linking.searchElastic("Vrije Universiteit Amsterdam")
    assert len(result.keys()) > 5


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
        "the 1970s",
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
