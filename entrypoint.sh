#!/bin/sh

while true; do
  # Execute the curl request and capture the HTTP status code
  http_status=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" \
    --data @/connectors/connector-config.json \
    http://casino-debezium:8083/connectors)

  # Check the HTTP status code
  case "$http_status" in
    200|201)
      echo "Success! The connector was created successfully."
      break
      ;;
    409)
      echo "Connector already exists. Exiting."
      break
      ;;
    *)
      echo "Failure (HTTP $http_status). Retrying..."
      sleep 2
      ;;
  esac
done