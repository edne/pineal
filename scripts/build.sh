#!/bin/bash
set -e

# load configuration
source build.cfg

# expand templates in _src/
scripts/expand.py

# move Python / Hy code in release folder
mkdir -p bin
cp -rf _src/py bin/

# confugure OpenFrameworks build system
projectGenerator -a"ofxOsc, ofxAubio" -o"$OF_PATH" .

rm -f config.make
echo "PROJECT_EXTERNAL_SOURCE_PATHS = $PY_INCLUDE" >> config.make

# actual code is in _src/
echo "PROJECT_EXCLUSIONS = \$(PROJECT_ROOT)/src%" >> config.make

echo "PROJECT_LDFLAGS = -lboost_python -L$PY_CONFIG -lpython2.7 -laubio" >> config.make
echo "PROJECT_CC = -Wall" >> config.make

# build
make

# cleanup
rm config.make addons.make *.qbs Makefile
rm -rf _src
