# Stop TimescaleDB instance and remove container
docker stop timescaledb
docker rm timescaledb
# Stop JupyterLab instance and remove container
docker stop jupyterlab
docker rm jupyterlab

docker network rm brick-portable-app
# cp bldg1-nobrick.ttl bldg1/bldg1.ttl
