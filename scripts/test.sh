#!/bin/sh

#make run & sleep 2 && python scripts/watch.py bin/data/test.pn 7172 /code
#exit 0

if scripts/generate.hy && make
then
    make run & sleep 2 && python scripts/watch.py bin/data/test.pn 7172 /code
fi
