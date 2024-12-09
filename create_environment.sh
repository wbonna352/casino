#! /bin/bash

docker network create casino-network

docker compose -f docker-compose-base.yml up -d

sleep 30

python src/db/models.py

curl -X POST -H "Content-Type: application/json" \
  --data @connectors/connector-config.json \
  http://localhost:8083/connectors


docker compose -f docker-compose-players.yml up -d