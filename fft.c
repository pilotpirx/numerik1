#include <gsl/gsl_complex.h>
#include <gsl/gsl_complex_math.h>
#include <malloc.h>
#include <stdlib.h>
#include <math.h>

#define PI 3.1415926535897932384626433832795028841971

void fft_recurse(gsl_complex *data, int length, int stride, gsl_complex *out)
{
    int k;
    gsl_complex *inner_out;

    if (length == 1) {
        out[0] = data[0];
        return;
    }

    inner_out = malloc(length * sizeof(gsl_complex));

    if (!inner_out) {
        exit(1);
    }

    fft_recurse(data, length / 2, stride * 2, inner_out);
    fft_recurse(data + stride, length / 2, stride * 2, inner_out + length / 2);

    for (k = 0; k < length / 2; k++) {
        out[k] =
                gsl_complex_add(
                        inner_out[k],
                        gsl_complex_mul(
                                inner_out[k + length / 2],
                                gsl_complex_polar(1, - 2 * PI * k / length)));
        out[k + length / 2] =
                gsl_complex_sub(
                        inner_out[k],
                        gsl_complex_mul(
                                inner_out[k + length / 2],
                                gsl_complex_polar(1, - 2 * PI * k / length)));
    }

    free(inner_out);
}

void fft(gsl_complex *data, int length)
{
    int k;
    double sqrt_N = sqrt(length);
    gsl_complex *out = malloc(length * sizeof(gsl_complex));
    fft_recurse(data, length, 1, out);
    for (k = 0; k < length; k++) {
        data[k] = gsl_complex_div_real(out[k], sqrt_N);
    }
    free(out);
}
