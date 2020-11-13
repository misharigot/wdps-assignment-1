import information_extraction as ie
import pytest

input_1 = """
    Neuro-linguistic programming (NLP) is a pseudoscientific approach to communication, 
    personal development, and psychotherapy created by Richard Bandler and John Grinder 
    in California, United States, in the 1970s.
    """


input_with_duplicate_entities = """
    This guy I know called Richard Bandler and some other text Richard Bandler in California!
    """


input_with_unwanted_entities = """
    This Fourth guy at 10:30 I know ten million called 34 Richard Bandler and $10.20 some fifth other 5.30 text Richard Bandler in California 1!
    """


# def test_get_entities():
#     actual = ie.get_nltk_entities(html["website-1"])
#     expected = [
#         ("ORGANIZATION", "NLP"),
#         ("PERSON", "Richard Bandler"),
#         ("PERSON", "John Grinder"),
#         ("GPE", "California"),
#         ("GPE", "United States"),
#     ]
#     assert actual == expected


@pytest.fixture
def information_extractor(monkeypatch):
    return ie.InformationExtractor()


def test_get_spacy_entities(information_extractor):
    actual = information_extractor.get_spacy_entities(input_1)
    expected = [
        "Richard Bandler",
        "NLP",
        "United States",
        "the 1970s",
        "John Grinder",
        "Neuro",
        "California",
    ]
    assert sorted(actual) == sorted(expected)


def test_get_spacy_entities_withduplicates(information_extractor):
    actual = information_extractor.get_spacy_entities(input_with_duplicate_entities)
    expected = [
        "Richard Bandler",
        "Richard Bandler",
        "California",
    ]
    assert sorted(actual) == sorted(expected)


def test_get_spacy_entities_without_unwanted_entities(information_extractor):
    actual = information_extractor.get_spacy_entities(input_with_unwanted_entities)
    expected = [
        "Richard Bandler",
        "Richard Bandler",
        "California",
    ]
    assert sorted(actual) == sorted(expected)
