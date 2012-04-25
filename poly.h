#ifndef POLY_H
#define POLY_H

double poly_neville(double* x, double* f, double t, int n);
void poly_neville_array(double *x, double *f, int n, double *t, double *out, int m);

double poly_de_casteljau(double *b, double t, int n);
void poly_de_casteljau_array(double *b, int n, double *t, double *out, int m)


#endif
