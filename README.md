# wdps-assignment-1

## Setting up the Docker environment

1. Build the image from the Dockerfile.

    ```sh
    docker build -t wdps_assignment:0.1.0 .
    ```

2. Run the container and mount your data folder.

    ```sh
    docker run -ti -v </PATH/TO/YOUR/DATA/FOLDER>:/app/assignment/data -p 9200:9200 wdps_assignment:0.1.0
    ```

3. Run the example

    ```sh
    ./src/run_example.sh
    ```
