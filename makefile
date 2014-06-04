all:
	gcc -Wall src/postprocessing.c -shared -opineal/postprocessing -fPIC
	./PinealLoopProject.py
	
