#!/bin/sh
set -e

scripts/build.sh

make run &
sleep 2 && python scripts/watch.py bin/data/test.pn 7172 /code
