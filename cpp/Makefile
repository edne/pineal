.PHONY: all clean test
.DEFAULT_GOAL = all

all: clean test

clean:
	rm *.o       || true
	rm *_wrap.*  || true
	rm *.so      || true
	rm *.pyc     || true
	rm pineal.py || true

test: _pineal.so test.py
	python test.py

_pineal.so: pineal.i pineal.cpp
	swig -c++ -python pineal.i
	g++ -fPIC -c pineal.cpp
	g++ -fPIC -c pineal_wrap.cxx -I/usr/include/python2.7
	g++ -shared pineal.o pineal_wrap.o -o _pineal.so

