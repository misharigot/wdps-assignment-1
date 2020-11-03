"""Preprocess the warc.gz files.
Output = refined text, maybe a dictionary of strings, e.g.:

{
    "website-1": [
        "Lorem ipsum dolor sit amet"
    ],
    "website-2": [
        "This", "is", "some", "other", "way", "of", "storing", "the", "data"
    ],
}

Stuff that could happen here is: 
- remove whitespace
- remove stopwords
- lemmetization
- word stemming
- etc.
"""

# import apache nlp?
