"""Information extraction: extracting the entities from the preprocessed data.
Output = textual entities & relations.
"""

from collections import Counter
from typing import Tuple

import en_core_web_md
import spacy
from spacy import displacy


class InformationExtractor:
    def __init__(self):
        self.nlp = en_core_web_md.load()

    def get_spacy_entities(self, text):
        with self.nlp.disable_pipes("tagger", "parser"):
            doc = self.nlp(text)
            result = [(X.label_, X.text) for X in doc.ents]
            result = self._apply_filters(result)
            return [x[1] for x in result]

    def _apply_filters(self, result):
        result = [
            r
            for r in result
            if r[0] != "CARDINAL"
            and r[0] != "TIME"
            and r[0] != "MONEY"
            and r[0] != "ORDINAL"
        ]
        return result
