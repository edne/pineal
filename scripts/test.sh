#!/bin/sh
set -e

# scripts/build.sh

bin/pineal &
python scripts/frontend.py examples/test.pn 7172
