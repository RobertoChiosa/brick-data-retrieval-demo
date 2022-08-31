# brick-data-retrieval-demo

This is a tutorial on how to perform queries on `.ttl` brick schema file using `jupiter` notebook and retrieve
the `uuid` of the relative timeseries froma a `timescaleDB` deployed locally on `docker` container.

In this folder is contained the code referring to the
repository [brick-data-retrieval-demo](https://github.com/gtfierro/brick-data-retrieval-demo) and explained
in [this tutorial video](https://www.youtube.com/watch?v=kZYNXoiM8gk)

## Setup

1. Compile the brick model. This is a necessary step to simplify queries on the model (to do only when the brick model
   changes).Execute the following command:
   ```bash 
   python compile.py bldg2.ttl
   ```

2. Create an `.env` file in the root directory and set up the environmental variables. All the scripts secrets have as
   reference the env file in the root folder and the file should be like the `example.env` file:
   ```bash 
   touch .env
   
   printf "TIMESCALEDB_HOST=timescaledb
   TIMESCALEDB_USER=postgres 
   TIMESCALEDB_PSW=mypassword 
   TIMESCALEDB_PORT=5432 
   POSTGRES_PASSWORD=mypassword 
   JUPYTER_TOKEN=mypassword" > .env
   ```

3. Unzip data files contained in `bldg2-data.zip`. Execute the following command:
    ```bash
    unzip bldg2-data.zip
    ```

4. Start docker containers. This action requires that you have [Docker](https://www.docker.com/) installed on your
   machine. Create containers by running the following command:
    ```bash
    ./scripts/start_docker_containers.sh
    ```
5. Check whether the docker containers are running through this command:
    ```bash
    docker ps
    ```

6. Load timeseries data in the timescal DB. This command creates the database schema and tables based on the
   script `schema.sql`
    ```bash
    ./scripts/setup.sh
    ```

## Data analysis

The data exploration process is performed through the jupiter notebook `DataRetrieval.ipynb`. A basic sparql query on
the brick schema is performed and data retrieval from the timescale db is performed.

## Shutdown

The `scripts/cleanup.sh` script will delete the docker containers and network and you can run the start/setup scripts
again
