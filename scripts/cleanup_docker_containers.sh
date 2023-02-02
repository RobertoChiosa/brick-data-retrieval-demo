# Stop TimescaleDB instance and remove container
docker stop timescaledb
echo "stopped timescaledb container"
docker rm timescaledb
echo "removed timescaledb container"

docker network rm brick-portable-app
echo "removed brick-portable-app network"
# cp bldg1-nobrick.ttl bldg1/bldg1.ttl
