#include <stdio.h>

#include "poly.h"


int main()
{
    double x1[] = {0,1,3};
    double y1[] = {1,3,2};
    
    printf("Beispiel 1.6 fuer t = %i: %g\n", 2, poly_neville(x1, y1, 2, 3));


    double x2[] = {0,1,2,4};
    double y2[] = {1,1,2,5};

    printf("Aufgabe 3a fuer t = 3: %g\n", poly_neville(x2, y2, 3, 4));

    double x3[] = {0,1,2,3,4};
    double y3[] = {1,1,2,3,5};

    printf("Aufgabe 3b fuer t = 5; %g\n", poly_neville(x3, y3, 5, 5));
    return 0;
}
