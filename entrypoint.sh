#!/bin/sh

while ! curl -s http://casino-debezium:8083/ &>/dev/null; do
  echo "Serwer niedostępny. Czekam..."
  sleep 2
done
curl -X POST -H "Content-Type: application/json" \
  --data @/connectors/connector-config.json \
  http://casino-debezium:8083/connectors