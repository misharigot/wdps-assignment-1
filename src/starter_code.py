import cProfile
import gzip
import pstats
import sys

import pandas as pd
from tqdm import tqdm

import information_extraction as ie
from nlp_preprocessing import preprocess_text
import entity_linking as el
from elasticsearch import Elasticsearch

KEYNAME = "WARC-TREC-ID"
KBPATH = "/app/assignment/assets/wikidata-20200203-truthy-uri-tridentdb"


class Executor:
    def __init__(self):
        self.entity_linking = el.Entity_Linking(KBPATH)
        self.information_extractor = ie.InformationExtractor()

    # The goal of this function is to process the webpage and to return a list of labels -> entity ID
    def _find_labels(self, payload):
        # print("step1, preprocessing")
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

        # print("step2, information extraction")
        entities = self.information_extractor.get_spacy_entities(text)

        # Problem 3: We now have to disambiguate the entities in the text. For instance, let's assugme that we identified
        # the entity "Michael Jordan". Which entity in Wikidata is the one that is referred to in the text?
        # print("step3, processing entities amount of : " + str(len(entities)))
        entity_wikidata = self.entity_linking.entityLinking(entities)
        # print("finished")
        for entity in entity_wikidata:
            yield key, entity[0], entity[1]

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

        # For now, we are cheating. We are going to returthe labels that we stored in sample-labels-cheat.txt
        # Instead of doing that, you should process the text to identify the entities. Your implementation should return
        # the discovered disambiguated entities with the same format so that I can check the performance of your program.
        # cheats = dict(
        #     (
        #         line.split("\t", 2)
        #         for line in open("../data/sample-labels-cheat.txt").read().splitlines()
        #     )
        # )
        # for label, wikidata_id in cheats.items():
        #     if key and (label in payload):
        #         yield key, label, wikidata_id

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
        # data = pd.DataFrame(columns=["key", "type", "label"])

        with gzip.open(warc_path, "rt", errors="ignore") as fo:
            counter = 0
            for record in tqdm(self.split_records(fo)):
                for key, label, wikidata_id in self._find_labels(record):
                    # row = {"key": key, "type": _type, "label": label}
                    # data = data.append(row, ignore_index=True)
                    print(key + "\t" + label + "\t" + wikidata_id)
                counter += 1
                if max_iterations and counter == max_iterations:
                    break
        # data.to_csv("result.csv")


if __name__ == "__main__":

    try:
        _, INPUT = sys.argv
    except Exception as e:
        print("Usage: python starter-code.py INPUT")
        sys.exit(0)

    executor = Executor()
    executor.execute(INPUT)

    # The following allows you to get performance stats on running execute()

    # cProfile.run('executor.execute()', 'restats')
    # p = pstats.Stats('restats')
    # p.sort_stats('cumulative').print_stats(30)
