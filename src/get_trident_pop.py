"""Utility function to obtain the popularity for an entity.
"""

import sys
import trident


def get_pop(url):
    db = trident.Db("/app/assignment/assets/wikidata-20200203-truthy-uri-tridentdb")

    id = db.lookup_id("<http://www.wikidata.org/entity/Q11268>")
    print(db.count_o(id))


if __name__ == "__main__":
    # Example usage:
    # python3 src/get_trident_pop.py "<http://www.wikidata.org/entity/Q11268>"

    try:
        _, INPUT = sys.argv
    except Exception as e:
        print("Usage: python3 get_trident_pop.py INPUT")
    get_pop(INPUT)
