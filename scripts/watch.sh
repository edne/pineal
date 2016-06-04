#!/bin/sh
set -e

export SERVER_ADDR=localhost:7172
export LISTEN_PORT=7173
export PINEAL_SERVER=./bin/pineal

touch .pineal_history

python src/client.py watch $1 
