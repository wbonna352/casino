#!/bin/bash

curl -X POST -H "Content-Type: application/json" \
  --data @connector-config.json \
  http://localhost:8083/connectors
