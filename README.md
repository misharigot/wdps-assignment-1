# wdps-assignment-1

## Prerequisites

- The assets and data directories from the large zip archives from the course.

## Building the docker image

You can build the image from the Dockerfile.

1. Clone repo and `cd` into it.
   ```sh
   git clone https://github.com/misharigot/wdps-assignment-1.git
   cd wdps-assignment-1
   ```

2. Build the image from the Dockerfile.

    ```sh
    docker build -t wdps_assignment:0.1.0 .
    ```

3. Add the assets and data directories from the large zip archives to the cloned repository. Making the following dir structure:

    ```
    .
    ├── assets
    │   ├── elasticsearch-7.9.2
    │   └── wikidata-20200203-truthy-uri-tridentdb
    ├── data
    │   ├── sample-labels-cheat.txt
    │   ├── sample.warc.gz
    │   ├── sample_annotations.tsv
    │   └── warcs
    |   ...
    ├── src
    │   └── ...
    └── test
        └── ...
    ```

4. Run the container and mount your data folder.

    ```sh
    docker run -ti -v /path/to/this/repo:/app/assignment -p 9200:9200 wdps_assignment:0.1.0
    ```

## Running the program

1. Start elastic search server.

    ```sh
    sh /app/assignment/src/start_elasticsearch_server.sh
    ```

1. Run the example

    ```sh
    sh /app/assignment/src/run_example.sh
    ```

1. Run pytest

    ```sh
    cd /app/assignment
    python3 -m pytest
    ```
