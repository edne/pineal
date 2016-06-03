#!/bin/sh
set -e

# scripts/build.sh
cp src/client.py bin/

export SERVER_ADDR=localhost:7172
export LISTEN_PORT=7173
export PINEAL_SERVER=./bin/pineal

touch .pineal_history

python bin/client.py test $(ls examples/*.pn) || echo "TEST FAILED"
