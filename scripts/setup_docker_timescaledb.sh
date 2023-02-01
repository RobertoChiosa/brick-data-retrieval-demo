# Exit the script immediately if a command returns a non-zero exit code.
set -e

# Load the schema into the TimescaleDB instance.
docker exec -i timescaledb psql -U postgres <scripts/schema.sql

# Copy data files into the container and load them into the database.
docker cp data timescaledb:/data

for csvfile in $(docker exec timescaledb /bin/ls /data); do
  # Copy the data from the csv file into the "data" table in the database.
  docker exec timescaledb psql -U postgres -c "\copy data(time,uuid,value) from /data/${csvfile} CSV HEADER;"
  # Remove the csv file after loading the data.
  docker exec timescaledb /bin/rm /data/${csvfile}
done
