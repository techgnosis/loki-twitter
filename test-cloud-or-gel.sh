#! /usr/bin/env bash

set -euo pipefail

curl \
-vvvv \
-H "Content-Type: application/json" \
-u "{$LOKI_USERNAME}":"{$LOKI_PASSWORD}" \
-d @test-data.json \
"{$LOKI_URL}"
