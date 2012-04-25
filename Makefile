all:
	gcc -Wall poly.c aufgabe01.c -o aufgabe01
	gcc -Wall -shared -fPIC poly.c -o libpoly.so