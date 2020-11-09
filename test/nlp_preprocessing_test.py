from nlp_preprocessing import preprocess_text

html = """
<html>
<p>this is a paragraph.</p>
</html>
"""

html_spanish = """
<html>
<p>este es un párrafo.</p>
</html>
"""

html_no_text = """
<html>
</html>
"""

def test_preprocess_text():
    actual = preprocess_text(html)
    expected = "this is a paragraph."

    assert actual == expected

def test_preprocess_text_dif_lang():
    actual = preprocess_text(html_spanish)

    assert actual == None

def test_preprocess_no_text():
    actual = preprocess_text(html_no_text)

    assert actual == None
