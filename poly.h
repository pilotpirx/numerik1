#ifndef POLY_H_
#define POLY_H_

double poly_neville(double* x, double* f, double t, int n);
void poly_neville_array(double *x, double *f, int n, double *t, double *out,
        int m);

double poly_de_casteljau(double *b, double t, int n, int n_deriv);
void poly_de_casteljau_array(double *b, int n, int n_deriv, double *t,
        double *out, int m);

#endif
