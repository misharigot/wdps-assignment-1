#!/bin/sh
echo "Processing webpages ..."
python3 /app/assignment/src/starter_code.py /app/assignment/data/sample.warc.gz > /app/assignment/sample_predictions.tsv
echo "Computing the scores ..."
python3 /app/assignment/src/score.py /app/assignment/data/sample_annotations.tsv /app/assignment/sample_predictions.tsv
