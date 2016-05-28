#!/bin/sh
set -e

# scripts/build.sh
cp -f src/client.py bin/  # client.py is not preprocessed

export SERVER_ADDR=localhost:7172
export LISTEN_PORT=7173

bin/pineal &
python src/client.py watch examples/test.pn
