.PHONY: all run clean build test
.DEFAULT_GOAL = all

SFML=-lsfml-graphics
LIBLO=-llo
LIBS=$(SFML) $(LIBLO)

CC=g++
LD=g++

WARN=-Wall -Wextra -Wpedantic -Wno-unused-parameter
CFLAGS=-fPIC -Wall -std=c++11 -Iinclude -I/usr/include/python2.7
LDFLAGS=$(LIBS) -shared

NAME=pineal

SRC_FILES=$(wildcard src/*.cpp) src/wrap.cpp
OBJ_FILES=$(patsubst src/%.cpp, obj/%.o, $(SRC_FILES))


all:
	mkdir obj  || true
	make clean
	make build
	make test

run:
	mkdir obj  || true
	make clean
	make build
	./pineal-run.py test/test.pn

clean:
	rm src/wrap.cpp        || true
	rm $(OBJ_FILES)        || true
	rm $(NAME)/_$(NAME).so || true
	rm $(NAME)/core.py     || true

build: $(NAME)/_$(NAME).so

test:
	nosetests -v

src/wrap.cpp: $(NAME).i
	swig -Wall -Wextra -Iinclude -module $(NAME) -c++ -python $<
	mv $(NAME)_wrap.cxx src/wrap.cpp
	mv $(NAME).py $(NAME)/core.py

obj/%.o: src/%.cpp
	$(CC) $(CFLAGS) -c $< -o $@

$(NAME)/_$(NAME).so: $(OBJ_FILES)
	$(LD) $(LDFLAGS) $(OBJ_FILES) -o $@
