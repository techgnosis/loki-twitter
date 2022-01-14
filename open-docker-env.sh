#! /usr/bin/env bash

set -euo pipefail

docker run -it --rm --name python -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3 bash
