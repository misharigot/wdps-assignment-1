# wdps-assignment-1

## Prerequisites

- The assets and data directories from the large zip archives from the course.

## Setting up the Docker environment

1. Clone repo and `cd` into it.

1. Build the image from the Dockerfile.

    ```sh
    docker build -t wdps_assignment:0.1.0 .
    ```

1. Add the assets and data directories from the large zip archives to the cloned repository.


1. Run the container and mount your data folder.

    ```sh
    docker run -ti -v /path/to/this/repo:/app/assignment -p 9200:9200 wdps_assignment:0.1.0
    ```

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
