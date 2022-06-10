#!/bin/bash

echo "STOPPING CONTAINERS"
docker stop $(docker ps -a -q)

echo "REBUILD IMAGES"
sleep 1
docker compose -f docker-compose.yml -f docker-compose.ci.yml build
#echo "... or not"

echo "RECREATE DB"
sleep 1
docker compose -f docker-compose.yml  up  --force-recreate -V -d database

echo "RUN TESTS"
sleep 1
# --wait-for-client
docker compose -f docker-compose.yml run backend poetry run python -m debugpy  --listen 0.0.0.0:5678 -m pytest 
pytest_units_status=$?
