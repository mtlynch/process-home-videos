#!/bin/bash

# Exit build script on first failure.
set -e

# Echo commands to stdout.
set -x

sudo apt-get update
sudo apt-get install \
  ffmpeg \
  python3 \
  python3-venv \
  --yes
python3 -m venv ./venv
. venv/bin/activate
pip install --requirement requirements.txt
./e2e/test-csv-to-yaml
VIDEOS_DIR=$(mktemp -d)
./e2e/test-render-scenes "$VIDEOS_DIR"
./e2e/test-publish-to-mediagoblin "$VIDEOS_DIR"