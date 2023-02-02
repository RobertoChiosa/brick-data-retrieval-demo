# brick-data-retrieval-demo

This is a tutorial on how to perform queries on `.ttl` brick schema file using `jupiter` notebook and retrieve
the `uuid` of the relative timeseries froma a `timescaleDB` deployed locally on `docker` container. The following figure
shows an example of result.

![Example of timeseries from query on timescald db and brick model](./img/download.png "Example of timeseries from query on timescald db and brick model")

In this folder is contained the code referring to the
repository [brick-data-retrieval-demo](https://github.com/gtfierro/brick-data-retrieval-demo) and explained
in [this tutorial video](https://www.youtube.com/watch?v=kZYNXoiM8gk)

## Setup

1. Create virtual environment in the root folder and activate
   ```bash 
   python3 -m venv venv
   ```
2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```

3. Create an `.env` file in the root directory and set up the environmental variables. All the scripts secrets have as
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

4. Unzip data files contained in `bldg2-data.zip`. Execute the following command:
    ```bash
    unzip data.zip
    ```

5. Start docker containers. This action requires that you have [Docker](https://www.docker.com/) installed on your
   machine. Create containers by running the following command:
    ```bash
    ./scripts/start_docker_containers.sh
    ```
6. Check whether the docker containers are running through this command:
    ```bash
    docker ps
    ```

7. Load timeseries data in the timescal DB. This command creates the database schema and tables based on the
   script `schema.sql`
    ```bash
    ./scripts/setup_docker_timescaledb.sh
    ```

## Maintenance

Export requirements

```bash
pipreqs . --force
```

## Data analysis

The data exploration process is performed through the jupiter notebook `DataRetrieval.ipynb`. A basic sparql query on
the brick schema and data retrieval from the timescale db is performed. Feel free to change the query, parameters and
variables to get different timeseries.

## Shutdown

The `scripts/cleanup.sh` script will delete the docker containers and network and you can run the start/setup scripts
again

```bash
./scripts/cleanup_docker_containers.sh
```
