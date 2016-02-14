#!/bin/sh
make
make run & sleep 1 && python bin/py/watch.py bin/data/test.pn 7172 /code
