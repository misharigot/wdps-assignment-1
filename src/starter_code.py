import cProfile
import gzip
import pstats
import sys
from typing import List

import pandas as pd
from elasticsearch import Elasticsearch
from tqdm import tqdm

import entity_linking as el
import information_extraction as ie
from nlp_preprocessing import preprocess_text

KEYNAME = "WARC-TREC-ID"
KBPATH = "/app/assignment/assets/wikidata-20200203-truthy-uri-tridentdb"


class Executor:
    def __init__(self):
        self.entity_linking = el.Entity_Linking(KBPATH)
        self.information_extractor = ie.InformationExtractor()

    # The goal of this function is to process the webpage and to return a list of labels -> entity ID
    def _find_labels(self, payload):
        if payload == "":
            return

        # The variable payload contains the source code of a webpage and some additional meta-data.
        # We first retrieve the ID of the webpage, which is indicated in a line that starts with KEYNAME.
        # The ID is contained in the variable 'key'
        key = None
        for line in payload.splitlines():
            if line.startswith(KEYNAME):
                key = line.split(": ")[1]
                break

        # Problem 1: The webpage is typically encoded in HTML format.
        # We should get rid of the HTML tags and retrieve the text. How can we do it?
        text = preprocess_text(payload)
        if text is None:
            return

        # Problem 2: Let's assume that we found a way to retrieve the text from a webpage. How can we recognize the
        # entities in the text?
        entities: List[str] = self.information_extractor.get_spacy_entities(text)

        # Problem 3: We now have to disambiguate the entities in the text. For instance, let's assugme that we identified
        # the entity "Michael Jordan". Which entity in Wikidata is the one that is referred to in the text?
        entity_wikidata = self.entity_linking.entity_linking(entities)
        for entity in entity_wikidata:
            yield key, entity[0], entity[1]

    @staticmethod
    def split_records(stream):
        payload = ""
        for line in stream:
            if line.strip() == "WARC/1.0":
                yield payload
                payload = ""
            else:
                payload += line
        yield payload

    def execute(
        self,
        warc_path: str = "/app/assignment/data/sample.warc.gz",
        max_iterations=None,
    ):
        with gzip.open(warc_path, "rt", errors="ignore") as fo:
            counter = 0
            for record in tqdm(self.split_records(fo)):
                for key, label, wikidata_id in self._find_labels(record):
                    print(key + "\t" + label + "\t" + wikidata_id)
                counter += 1
                if max_iterations and counter == max_iterations:
                    break


if __name__ == "__main__":
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print("Usage: python starter-code.py INPUT")
        INPUT = "/app/assignment/data/sample.warc.gz"

    executor = Executor()
    executor.execute(INPUT)
