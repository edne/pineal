#!/bin/sh
make
make run & sleep 3 && python bin/py/watch.py bin/data/test.pn 7172 /code
