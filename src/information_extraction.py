"""Information extraction: extracting the entities from the preprocessed data.
Output = textual entities & relations.
"""

# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag
# from nltk.chunk import ne_chunk

from collections import Counter
from typing import Tuple

import en_core_web_md
import spacy
from spacy import displacy

# def get_nltk_entities(text):
#     ne_tree = ne_chunk(pos_tag(word_tokenize(text)))
#     result = []
#     for chunk in ne_tree:
#         if hasattr(chunk, "label"):
#             label = chunk.label()
#             entity = " ".join(c[0] for c in chunk)
#             result.append((label, entity))
#     return result


class InformationExtractor:
    def __init__(self):
        self.nlp = en_core_web_md.load()

    def get_spacy_entities(self, text):
        with self.nlp.disable_pipes("tagger", "parser"):
            doc = self.nlp(text)
            result = [X.text for X in doc.ents]
            return list(set(result))
