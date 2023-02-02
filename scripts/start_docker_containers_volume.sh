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
  -v "$VOLUME_NAME$":/var/lib/postgresql/data \
  timescale/timescaledb:latest-pg12
