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


input_with_numbers_and_time = """
    This guy at 10:30 I know called 34 Richard Bandler and some other text Richard Bandler in California 1!
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
    assert set(actual) == set(expected)


def test_get_spacy_entities_without_duplicates(information_extractor):
    actual = information_extractor.get_spacy_entities(input_with_duplicate_entities)
    expected = [
        "Richard Bandler",
        "California",
    ]
    assert set(actual) == set(expected)


def test_get_spacy_entities_without_mumbers(information_extractor):
    actual = information_extractor.get_spacy_entities(input_with_numbers_and_time)
    expected = [
        "Richard Bandler",
        "California",
    ]
    assert set(actual) == set(expected)
