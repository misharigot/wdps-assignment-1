from src.information_extraction import get_entities

html = {
    "website-1": """
    Neuro-linguistic programming (NLP) is a pseudoscientific approach to communication, 
    personal development, and psychotherapy created by Richard Bandler and John Grinder 
    in California, United States, in the 1970s.
    """
}


def test_get_entities():
    actual = get_entities(html["website-1"])
    expected = [
        ('ORGANIZATION', 'NLP'), 
        ('PERSON', 'Richard Bandler'), 
        ('PERSON', 'John Grinder'), 
        ('GPE', 'California'), 
        ('GPE', 'United States')
    ]
    assert actual == expected
