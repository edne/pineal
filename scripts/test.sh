#!/bin/sh
set -e

# scripts/build.sh

bin/pineal &
python bin/client.py examples/test.pn 7172
