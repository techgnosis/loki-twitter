#! /usr/bin/env bash

set -euo pipefail

curl \
-vvvv \
-H "Content-Type: application/json" \
-u $GEL_TENANT:"{$GEL_TOKEN}" \
-d @test-data.json \
https://gel.lab.home/loki/api/v1/push
