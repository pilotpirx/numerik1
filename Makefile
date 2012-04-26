
default : a01

poly.o : poly.c
	gcc -Wall -fPIC -c -o poly.o poly.c

libpoly.so : poly.o
	gcc -shared -o libpoly.so poly.o

aufgabe01 : poly.o aufgabe01.c
	gcc -o aufgabe01 aufgabe01.c poly.o

a01 : aufgabe01 libpoly.so

clean : 
	rm *.so aufgabe01 *.o \#* *~


