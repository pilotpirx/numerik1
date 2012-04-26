#include <malloc.h>
#include <stdlib.h>

#include "poly.h"

double poly_neville(double *x, double *f, double t, int n)
{
    double* array = malloc(n * sizeof(double));
    int i, j;
    double temp;
    
    for(i = 0; i < n; i++){
	array[i] = f[i];
	for (j = i - 1; j >= 0; j--){
	    array[j] = (t - x[j]) * array[j + 1] - (t - x[i]) * array[j];
	    array[j] /= x[i] - x[j];
	}
    }

    temp = array[0];
    free(array);
    return(temp);
}

void poly_neville_array(double *x, double *f, int n, double *t, double *out, int m)
{
    int i;

    for (i = 0; i < m; i++) {
	out[i] = poly_neville(x, f, t[i], n);
    }
}


double poly_de_casteljau(double *b, double t, int n)
{
    double *array = malloc(n * sizeof(double));
    if (!array) {
	exit(1);
    }

    int i, j;
    double tmp;

    for (i = 0; i < n; i++) {
	array[i] = b[i];
    }

    for (i = 1; i < n; i++) {
	for (j = 0; j < n - i; j++) {
	    array[j] = t * array[j + 1] + (1 - t) * array[j];
	}
    }

    tmp = array[0];
    free(array);
    return tmp;
}


void poly_de_casteljau_array(double *b, int n, double *t, double *out, int m)
{
    int i;
    
    for (i = 0; i < m; i++) {
	out[i] = poly_de_casteljau(b, t[i], n);
    }
}
