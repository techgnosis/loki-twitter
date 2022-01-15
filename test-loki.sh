#! /usr/bin/env bash

set -euo pipefail

curl \
-vvvv \
-H "Content-Type: application/json" \
-H "X-Scope-OrgID: fake" \
-d @test-data.json \
"{$LOKI_URL}"
