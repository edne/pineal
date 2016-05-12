#!/bin/sh

scripts/generate.py
cp -rf src/py bin/
make
