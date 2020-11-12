import cProfile
import gzip
import pstats
import sys
from typing import Tuple

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
        self.entity_linking = el.Entity_Linking(KBPATH, strategy="query_string")
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

        entities = self.information_extractor.get_spacy_entities(text)
        enriched_entities = self.entity_linking.enrich_entities(entities)

        # Problem 3: We now have to disambiguate the entities in the text. For instance, let's assume that we identified
        # the entity "Michael Jordan". Which entity in Wikidata is the one that is referred to in the text?

        for enriched_entity in enriched_entities:
            disambiguated_entity = self.disambiguate(enriched_entity, text)
            if disambiguated_entity:
                wikidata_id = disambiguated_entity[0]
                label = disambiguated_entity[1]
                yield key, label, wikidata_id

        # To tackle this problem, you have access to two tools that can be useful. The first is a SPARQL engine (Trident)
        # with a local copy of Wikidata. The file "test_sparql.py" shows how you can execute SPARQL queries to retrieve
        # valuable knowledge. Please be aware that a SPARQL engine is not the best tool in case you want to lookup for
        # some strings. For this task, you can use elasticsearch, which is also installed in the docker image.
        # The file start_elasticsearch_server.sh will start the elasticsearch server while the file
        # test_elasticsearch_server.py shows how you can query the engine.

        # A simple implementation would be to first query elasticsearch to retrieve all the entities with a label
        # that is similar to the text found in the web page. Then, you can access the SPARQL engine to retrieve valuable
        # knowledge that can help you to disambiguate the entity. For instance, if you know that the webpage refers to persons
        # then you can query the knowledge base to filter out all the entities that are not persons...

        # Obviously, more sophisticated implementations that the one suggested above are more than welcome :-)

    def disambiguate(self, enriched_entity: Tuple[str, str, str], text):
        """enriced_entity = (label, name, description)"""
        similarities = []  # wiki_url, sim_score, entity_label
        for wiki_url, enrichment in enriched_entity.items():
            """
            {
                '<http://www.wikidata.org/entity/Q65026858>':
                    ('France', 'print in the National Gallery of Art (NGA 30406)'),
                '<http://www.wikidata.org/entity/Q64582899>':
                    ('France', 'drawing in the National Gallery of Art (NGA 67958)')
            }
            """
            entity_label = enrichment[1]
            entity_name = enrichment[0]
            entity_description = enrichment[2]

            similarity_score = self.get_jaccard_sim(entity_description, text)
            similarities.append((wiki_url, similarity_score, entity_label, entity_name))

        # Get highest similarity and add to list
        if len(similarities) > 0:
            similarities = sorted(similarities, key=lambda x: x[1])
            most_similar = similarities[0]
            url = most_similar[0]
            label = most_similar[2]
            return url, label

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

    @staticmethod
    def get_jaccard_sim(str1, str2):
        a = set(str1.split())
        b = set(str2.split())
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    def execute(
        self,
        warc_path: str = "/app/assignment/data/sample.warc.gz",
        max_iterations=None,
    ) -> pd.DataFrame:
        data = pd.DataFrame(columns=["key", "type", "label"])

        with gzip.open(warc_path, "rt", errors="ignore") as fo:
            counter = 0
            for record in tqdm(self.split_records(fo)):
                for key, label, wikidata_id in self._find_labels(record):
                    # Output as expected by assignment requirements:
                    print(key + "\t" + label + "\t" + wikidata_id)

                    row = {"key": key, "label": label, "wikidata_id": wikidata_id}
                    data = data.append(row, ignore_index=True)
                counter += 1
                if max_iterations and counter == max_iterations:
                    break
        return data


if __name__ == "__main__":

    try:
        _, INPUT = sys.argv
    except Exception as e:
        print("Usage: python starter-code.py INPUT")
        INPUT = "/app/assignment/data/sample.warc.gz"

    executor = Executor()
    data = executor.execute(INPUT)
    print(data)
    # data.to_csv("result.csv")

    # The following allows you to get performance stats on running execute()

    # cProfile.run('executor.execute()', 'restats')
    # p = pstats.Stats('restats')
    # p.sort_stats('cumulative').print_stats(30)
