#! /usr/bin/env bash

set -euo pipefail

kapp deploy -a loki-twitter \
-f deployment.yaml
