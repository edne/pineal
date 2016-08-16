#!/bin/bash
set -e

# load configuration
source build.cfg

# move Python / Hy code in release folder
mkdir -p bin
cp -rf src/libs bin/

# confugure OpenFrameworks build system
projectGenerator -a"ofxOsc, ofxAubio" -o"$OF_PATH" .

rm -f config.make
echo "PROJECT_EXTERNAL_SOURCE_PATHS = $PY_INCLUDE" >> config.make

echo "PROJECT_LDFLAGS = -lboost_python -L$PY_CONFIG -lpython2.7 -laubio" >> config.make
echo "PROJECT_CC = -Wall" >> config.make

# build
make

# cleanup
rm config.make addons.make *.qbs Makefile
