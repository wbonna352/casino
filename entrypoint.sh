#!/bin/sh

while true; do
  # Execute the curl request with --fail
  curl --fail -X POST -H "Content-Type: application/json" \
    --data @/connectors/connector-config.json \
    http://casino-debezium:8083/connectors

  # Check the exit status
  if [ $? -eq 0 ]; then
    echo "Success! The command executed correctly."
    break
  else
    echo "Failure. Retrying..."
    sleep 2 # Optional delay between retries
  fi
done