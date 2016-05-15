#!/bin/sh
set -e

scripts/build.sh

bin/pineal &
python scripts/frontend.py bin/data/test.pn 7172
