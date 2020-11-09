import information_extraction as ie

html = {
    "website-1": """
    Neuro-linguistic programming (NLP) is a pseudoscientific approach to communication, 
    personal development, and psychotherapy created by Richard Bandler and John Grinder 
    in California, United States, in the 1970s.
    """
}


def test_get_entities():
    actual = ie.get_nltk_entities(html["website-1"])
    expected = [
        ("ORGANIZATION", "NLP"),
        ("PERSON", "Richard Bandler"),
        ("PERSON", "John Grinder"),
        ("GPE", "California"),
        ("GPE", "United States"),
    ]
    assert actual == expected


def test_get_spacy_entities():
    actual = ie.get_spacy_entities(html["website-1"])
    expected = [
        ("ORG", "Neuro"),
        ("ORG", "NLP"),
        ("PERSON", "Richard Bandler"),
        ("PERSON", "John Grinder"),
        ("GPE", "California"),
        ("GPE", "United States"),
        ("DATE", "the 1970s"),
    ]
    assert actual == expected
