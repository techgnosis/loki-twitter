#! /usr/bin/env bash

set -euo pipefail

k create secret generic loki-twitter \
--namespace loki-twitter \
--from-literal=loki_url="" \
--from-literal=loki_username="" \
--from-literal=loki_password="" \
--from-literal=twitter_bearer_token=""