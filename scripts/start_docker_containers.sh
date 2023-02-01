# Export environment variables from the .env file, excluding commented lines.
export $(grep -v '^#' .env | xargs)

# Create a custom Docker network "brick-portable-app".
docker network create brick-portable-app

# Start a TimescaleDB instance in detached mode (-d) with a custom network "brick-portable-app".
# Map host IP 127.0.0.1 to container port 5432 and expose it on host port 5432.
# Set the POSTGRES_PASSWORD environment variable.
# Use the latest-pg12 version of the TimescaleDB image.
docker run -d \
  --net brick-portable-app \
  --name timescaledb \
  -p 127.0.0.1:5432:5432 \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  timescale/timescaledb:latest-pg12

# Start a JupyterLab instance in detached mode (-d) with a custom network "brick-portable-app".
# Map host port 8080 to container port 8080 and host port 8888 to container port 8888.
# Set the JUPYTER_ENABLE_LAB environment variable to "yes".
# Mount the current working directory as "/home/jovyan" in the container.
# Use the Jupyter datascience-notebook image.
# Run the start-notebook.sh script with the JUPYTER_TOKEN environment variable.
docker run -d \
  --net brick-portable-app \
  --name jupyterlab \
  -p 8080:8080 \
  -p 8888:8888 \
  -e JUPYTER_ENABLE_LAB=yes \
  -v "$PWD":/home/jovyan \
  jupyter/datascience-notebook \
  start-notebook.sh \
  --NotebookApp.token="$JUPYTER_TOKEN"
