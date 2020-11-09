"""Information extraction: extracting the entities from the preprocessed data.
Output = textual entities & relations.
"""

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_md


def get_nltk_entities(text):
    ne_tree = ne_chunk(pos_tag(word_tokenize(text)))
    result = []
    for chunk in ne_tree:
        if hasattr(chunk, "label"):
            label = chunk.label()
            entity = " ".join(c[0] for c in chunk)
            result.append((label, entity))
    return result


def get_spacy_entities(text):
    nlp = en_core_web_md.load()
    doc = nlp(text)
    result = [(X.label_, X.text) for X in doc.ents]
    return result
