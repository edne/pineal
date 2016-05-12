#!/bin/sh
set -e

scripts/build.sh

bin/pineal &
sleep 2 && python scripts/watch.py bin/data/test.pn 7172 /code
