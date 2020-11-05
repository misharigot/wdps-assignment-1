"""Information extraction: extracting the entities from the preprocessed data.
Output = textual entities & relations.
"""

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import  ne_chunk

def get_entities(text):
    ne_tree = ne_chunk(pos_tag(word_tokenize(text)))
    entities = []
    for chunk in ne_tree:
        if hasattr(chunk, 'label'):
            label = chunk.label()
            entity = ' '.join(c[0] for c in chunk)
            entities.append((label, entity))
    return entities
