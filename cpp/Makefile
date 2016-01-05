.PHONY: all clean build test
.DEFAULT_GOAL = all

SFML=-lsfml-graphics
LIBLO=-llo
LIBS=$(SFML) $(LIBLO)

CC=g++
LD=g++

CFLAGS=-fPIC -Wall -std=c++11 -Iinclude -I/usr/include/python2.7
LDFLAGS=$(LIBS) -shared

NAME=pineal

SRC_FILES=$(wildcard src/*.cpp) src/wrap.cpp
OBJ_FILES=$(patsubst src/%.cpp, obj/%.o, $(SRC_FILES))


all:
	make clean
	make build
	python test.py

clean:
	rm src/wrap.cpp        || true
	rm $(OBJ_FILES)        || true
	rm $(NAME)/_$(NAME).so || true
	rm $(NAME)/__init__.py || true

build: $(NAME)/_$(NAME).so

test: build test.py
	python test.py

src/wrap.cpp: $(NAME).i
	swig -Wall -Iinclude -module $(NAME) -c++ -python $<
	mv $(NAME)_wrap.cxx src/wrap.cpp
	mv $(NAME).py $(NAME)/__init__.py

obj/%.o: src/%.cpp
	$(CC) $(CFLAGS) -c $< -o $@

$(NAME)/_$(NAME).so: $(OBJ_FILES)
	$(LD) $(LDFLAGS) $(OBJ_FILES) -o $@
